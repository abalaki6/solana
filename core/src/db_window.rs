//! Set of functions for emulating windowing functions from a database ledger implementation
use crate::blocktree::*;
use crate::packet::{SharedBlob, BLOB_HEADER_SIZE};
use crate::result::Result;
use crate::streamer::BlobSender;
use solana_metrics::counter::Counter;
use solana_sdk::pubkey::Pubkey;
use std::borrow::Borrow;
use std::sync::Arc;

pub const MAX_REPAIR_LENGTH: usize = 128;

pub fn retransmit_blobs(dq: &[SharedBlob], retransmit: &BlobSender, id: &Pubkey) -> Result<()> {
    let mut retransmit_queue: Vec<SharedBlob> = Vec::new();
    for b in dq {
        // Don't add blobs generated by this node to the retransmit queue
        if b.read().unwrap().id() != *id {
            retransmit_queue.push(b.clone());
        }
    }

    if !retransmit_queue.is_empty() {
        inc_new_counter_info!("streamer-recv_window-retransmit", retransmit_queue.len());
        retransmit.send(retransmit_queue)?;
    }
    Ok(())
}

/// Process a blob: Add blob to the ledger window.
pub fn process_blob(blocktree: &Arc<Blocktree>, blob: &SharedBlob) -> Result<()> {
    let is_coding = blob.read().unwrap().is_coding();

    // Check if the blob is in the range of our known leaders. If not, we return.
    let (slot, pix) = {
        let r_blob = blob.read().unwrap();
        (r_blob.slot(), r_blob.index())
    };

    // TODO: Once the original leader signature is added to the blob, make sure that
    // the blob was originally generated by the expected leader for this slot

    // Insert the new blob into block tree
    if is_coding {
        let blob = &blob.read().unwrap();
        blocktree.put_coding_blob_bytes(slot, pix, &blob.data[..BLOB_HEADER_SIZE + blob.size()])?;
    } else {
        blocktree.insert_data_blobs(vec![(*blob.read().unwrap()).borrow()])?;
    }

    Ok(())
}

#[cfg(test)]
mod test {
    use super::*;
    use crate::blocktree::get_tmp_ledger_path;
    use crate::entry::{make_tiny_test_entries, EntrySlice};
    use crate::packet::index_blobs;
    use std::sync::Arc;

    #[test]
    fn test_process_blob() {
        let blocktree_path = get_tmp_ledger_path!();
        let blocktree = Arc::new(Blocktree::open(&blocktree_path).unwrap());
        let num_entries = 10;
        let original_entries = make_tiny_test_entries(num_entries);
        let shared_blobs = original_entries.clone().to_shared_blobs();

        index_blobs(&shared_blobs, &Pubkey::new_rand(), 0, 0, 0);

        for blob in shared_blobs.iter().rev() {
            process_blob(&blocktree, blob).expect("Expect successful processing of blob");
        }

        assert_eq!(
            blocktree.get_slot_entries(0, 0, None).unwrap(),
            original_entries
        );

        drop(blocktree);
        Blocktree::destroy(&blocktree_path).expect("Expected successful database destruction");
    }
}
