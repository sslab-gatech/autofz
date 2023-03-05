<?php

abstract class A           { abstract function bar($x, $y = 0); }
abstract class B extends A { abstract function bar($x); }

echo "DONE";
?>