const Sequelize = require('sequelize');

const sequelize = new Sequelize('mysql://vvxtcvmokxseyjqv:hiqv5ffdcrz6kw8u@o3iyl77734b9n3tg.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/fx3yyf3htrppgcde', {
  logging: false
});

sequelize
  .authenticate()
  .then(function(){
    console.log('success');
  })
  .catch(function(err) {
    console.log(err.message);
  });

sequelize.sync({force: true}).then();

module.exports = {
  Sequelize,
  sequelize
}
