<?php

abstract class Foo {
    abstract public function __construct();
}

class Bar extends Foo {
    public function __construct(){}
}

class Baz extends Bar {
    protected function __construct(){}
}