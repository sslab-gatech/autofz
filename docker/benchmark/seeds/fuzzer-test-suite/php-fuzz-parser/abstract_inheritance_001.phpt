<?php

abstract class A           { abstract function bar($x); }
abstract class B extends A { abstract function bar($x); }

echo "DONE";
?>