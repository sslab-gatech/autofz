<?php

const VALUE = true;

trait Foo {public $var = VALUE;}
trait Bar {public $var = VALUE;}
class Baz {use Foo, Bar;}

echo "DONE";

?>