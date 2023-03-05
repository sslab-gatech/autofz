<?php
class Whatever {}
class Thing extends Whatever {}

class Foo {
    public Whatever $qux;
}

class Bar extends Foo {
    public Thing $qux;
}
?>