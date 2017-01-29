// Create a new instance of node-core-audio 
var coreAudio = require("node-core-audio");


function processAudio( inputBuffer ) {
    // Just print the value of the first sample on the left channel 
    console.log( inputBuffer[0][0] );
}



var engine = coreAudio.createNewAudioEngine();
 
engine.addAudioCallback( processAudio );


// Grab a buffer 
var buffer = engine.read();
 
// Silence the 0th channel 
for( var iSample=0; iSample<inputBuffer[0].length; ++iSample )
    buffer[0][iSample] = 0.0;
 
// Send the buffer back to the sound card 
engine.write( buffer );