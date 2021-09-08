function checkRequirements()
	{
		try {
			var fr = new FileReader();
			if( Uint8Array !== undefined 
					&&  Blob !== undefined 
					&&  ArrayBuffer !== undefined 
					&&  fr.readAsArrayBuffer !== undefined 
					&&  window.URL !== undefined 
					&&  window.URL.createObjectURL !== undefined ) {
				return true;
			}
		}
		catch( ex ) {}
		
		return false;
	}

var FileUtils = {
	getIntAt: function( arr, offs ) 
	{
		return (arr[offs+3] << 24) +
			   (arr[offs+2] << 16) +
			   (arr[offs+1] << 8) +
				arr[offs+0];
	},
	getWordAt: function( arr, offs ) 
	{
		return (arr[offs+1] << 8) +
				arr[offs+0];
	}
};

function PkgReaderV1()
{
	this.readPtr = 9;
	this.fileCount = 0;
}

PkgReaderV1.prototype = {
	readInt: function( arr )
	{
		var i = FileUtils.getIntAt( arr, this.readPtr );
		this.readPtr += 4;
		return i;
	},					
	readWord: function( arr )
	{
		var i = FileUtils.getWordAt( arr, this.readPtr );
		this.readPtr += 8;
		return i;
	},					
	readStr: function( arr )
	{
		var offs = this.readPtr;
		var i = this.readInt( arr );
		var arrString = arr.slice( offs + 4, offs + 4 + i );
		
		this.readPtr += i;
		
		var string = new TextDecoder("utf-8").decode( arrString );
		
		return string;
	},					
	readBinary: function( arr )
	{
		var offs = this.readPtr;
		var i = arrString( arr );
		var arrString = arr.slice( offs + 4, offs + 4 + i );
		
		this.readPtr += i;
		
		return arrString;
	},					
	readFile: function( content, offset, length )
	{
		return function(resolve, reject) {
			setTimeout( function() {
				try {
					var result = new Blob([content.slice( offset, offset + length )]);
					resolve( result );
					return;
				}
				catch( ex ){}
				reject();
			}, 100 );
		};
	},
	readVersionString: function( content )
	{
		this.readPtr = 0;
		this.fileCount = 0;
		
		// check version
		var ver = this.readStr( content );
		return ver;
	},
	decodeFile: function( content )
	{
		var self = this;
		
		//var content = e.target.result;
		//content = new Uint8Array( e.target.result );
		
		this.readPtr = 0;
		this.fileCount = 0;
		
		// check version
		var ver = this.readStr( content );
		if( ver !== 'PKGV0001' && ver !== 'PKGV0002' && ver !== 'PKGV0003' && ver !== 'PKGV0004' ) 
		{
			// disable version checking 
			//$("#file").closest('.card-body').show();
			//alert( "Decoder does not support this pkg version" );
			//return;
		}
		
		var files = [];
		this.fileCount = this.readInt( content );
		console.log( 'this.fileCount', this.fileCount );
		for( var i = 0 ; i < this.fileCount; i++ )
		{
			var fn = {
				name: this.readStr( content ),
				offset: this.readInt( content ),
				size: this.readInt( content )
			};
			files.push( fn );
		}
		
		var readers = [];
		
		var filesToRead = files.slice( 0 );
		
		var fnComplete = function()
		{
			var zip = new JSZip();
			for( var i in files ) 
			{
				var fn = files[ i ];
				zip.file( fn.name, fn.content );
			}
			zip.generateAsync({type:"blob"})
				.then(function(content) {
					// see FileSaver.js
					var url = window.URL.createObjectURL( content );
					//console.log( url );
					//saveAs(content, "example.zip");

					var a = document.createElement("a");
					a.href = url;
					a.className = 'btn btn-primary';
					a.download = 'scene.zip';
					a.innerText = "Download Scene.zip ( " + ( content.size / 1024 ).toFixed(1) + 'KB )';

					document.getElementById('downloadlink').innerHTML = '';
					document.getElementById('downloadlink').appendChild(a);

				});
		};
		
		var cnt = 1;
		var fnNext = function() {
			if( filesToRead.length ) 
			{
				var fn = filesToRead.shift();
				$("#downloadlink").text( "Reading file " + cnt++ + " of " + files.length );
				
				console.log( 'next file: ', fn.name, fn.size );
				fn.content = new Blob([content.slice( self.readPtr + fn.offset, self.readPtr + fn.offset + fn.size )]);	
				setTimeout( fnNext, 50 );
			}
			else 
			{
				$("#file").closest('.card-body').show();
				fnComplete();
			}
		};
		
		console.log( 'start reading', files );
		setTimeout( fnNext, 100 );
		
	}
}

function main() {
	
	var decoderV1 = new PkgReaderV1();				
	
	if( checkRequirements() ) {
		$('#supported').show();
		$('#not-supported').hide();
	}
	else {
		$('#supported').hide();
		$('#not-supported').show();
		return;
	}
	
	
	$("#file").on('change', function( e ) {
		$("#file").closest('.card-body').hide();
		
		document.getElementById('downloadlink').innerHTML = '';
		//console.log(  document.getElementById("file").files[0] );
		
		var fr = new FileReader();
		fr.onload = function( e ) { 
			
			var content = new Uint8Array( e.target.result );
			
			var version = decoderV1.readVersionString( content );
			switch( version ) 
			{
				case 'PKGV0001':
				case 'PKGV0002':
				case 'PKGV0003':
				case 'PKGV0004':
				default: // disabled version check
					decoderV1.decodeFile( content ) ;
					break;
					
				//case 'PKGV0003': // in case it ever exists 
					// decoder = new decoder();
					// decoder.decodeFile( content );
					
				// disable version checking 
				//default:
					//$("#file").closest('.card-body').show();
					//alert( "Unsupported Version" );
					//break;
			}
		};
		fr.readAsArrayBuffer( document.getElementById("file").files[0] );
		
		document.getElementById("file").value = '';
	});
})