<?php

class Foo {
    public function test(): Stringable {}
}
class Bar extends Foo {
    public function test(): Bar {}
    public function __toString() {}
}

?>
===DONE===