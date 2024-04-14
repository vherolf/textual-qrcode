"""Provides a QR code widget."""

##############################################################################
# Python imports.
from typing       import Any, cast
from urllib.parse import quote

##############################################################################
# qr lib imports.
import segno

##############################################################################
# Textual imports.
from textual.widgets import Static
from textual.message import Message

##############################################################################
class QRCode( Static ):
    """A simple text-based QR code widget.

    **NOTE:** This is a wrapper around https://qrenco.de/ -- anything you
    encode with this widget will be sent to that site.

    **NOTE:** This widget, due to the nature of what it's designed to
    display, will change width and height depending on the data it is asked
    to display.
    """

    DEFAULT_CSS = """QRCode { width: 0; height: 0; }"""
    """str: The default CSS for the widget."""

    def __init__( self, text: str, *args: Any, **kwargs: Any ) -> None:
        """Initialise the QR code widget.

        Args:
            text (str): The text to encode.
        """
        super().__init__( *args, **kwargs )
        self._content              = text
        self._qr_code: list[ str ] = []

    def encode( self, text: str ) -> None:
        """Encode some new text.

        Args:
            text (str): The text to encode.
        """
        self._content = text
        self._qr_code = []
        self.call_later( self._get_qr_code )

    @property
    def encoded_content( self ) -> str:
        """str: The content that was encoded in the QR code."""
        return self._content

    class _Message( Message ):
        """Base message sent out by the QR code widget."""

        @property
        def qr_code( self ) -> "QRCode":
            """QRCode: The QR code widget sending the message."""
            return cast( QRCode, self.sender )

    class Encoded( _Message ):
        """A message sent when the content was encoded without a problem."""

    class Error( _Message ):
        """A message sent when there was an error encoding the content.

        Attributes:
            error (Exception): The exception that is the cause of the error.
        """

        def __init__( self, error: Exception, *args: Any, **kwargs: Any ) -> None:
            """Initialise the error message.

            Args:
                error (Exception): The exception that describes the error.
            """
            super().__init__( *args, **kwargs )
            self.error = error

    async def _get_qr_code( self ) -> None:
        qrcode = segno.make(self.encoded_content.strip(),micro=False)
        qrcode.save('test.ans') 

        self._qr_code = open("test.ans","r").read()
        
        self.styles.width  = len(self._qr_code)
        self.styles.height = len(self._qr_code)
        
        self.update( self._qr_code  )

### qrcode.py ends here
