const sequelize = require('./sql').sequelize;
const Datatypes = require('./sql').Sequelize;

const NODES_TEST = sequelize.define('NODES_TEST', {
  ip_addr: {
    type: Datatypes.INTEGER,
    allowNull: false,
    defaultValue: 0
  },
  longtitude: {
    type: Datatypes.FLOAT,
    allowNull: false,
    defaultValue: -1
  },
  latitude: {
    type: Datatypes.FLOAT,
    allowNull: false,
    defaultValue: -1
  },
  city:{
    type: Datatypes.STRING,
    allowNull: false,
  },
  region:{
    type: Datatypes.STRING,
    allowNull: false,
  },
  country:{
    type: Datatypes.STRING,
    allowNull: false,
  },
  ping_time:{
    type: Datatypes.INTEGER,
    allowNull: false,
    defaultValue: 0
  },
  slot_height:{
    type: Datatypes.INTEGER,
    allowNull: false,
    defaultValue: 0
  },
  transaction_count:{
    type: Datatypes.INTEGER,
    allowNull: false,
    defaultValue: 0
  },
  stake_weight:{
    type: Datatypes.FLOAT,
    allowNull: false,
    defaultValue: 0
  },
  public_key:{
    type: Datatypes.STRING,
    allowNull: false,
    defaultValue:''
  },
  socket_status:{
    type: Datatypes.INTEGER,
    allowNull: false,
    defaultValue: 255
  }
});

module.exports = NODES_TEST;
