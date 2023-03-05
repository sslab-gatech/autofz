<?php

require('bug74922b.inc');

trait T2 {public $var = Bug74922\FOO;}
class Baz {use Bug74922\T1, T2;}

echo "DONE";

?>