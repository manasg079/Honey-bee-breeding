const EventEmitter = require('events');
const emitter=new EventEmitter();
emitter.on('start',()=>{
    console.log('Event triggerered');
});
emitter.emit('start');

const colours = ["red","yellow","green","blue"];
console.log(colours);
console.log(colours.length);

var upp_ch=require('upper-case');
console.log(upp_ch.upperCase("i am proud of you"));