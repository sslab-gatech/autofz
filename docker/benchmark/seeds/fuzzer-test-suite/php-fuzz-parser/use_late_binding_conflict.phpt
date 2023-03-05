<?php

/* Reverse declaration order disables early-binding */
class B extends A {}
class A {}
use Foo\B;

?>