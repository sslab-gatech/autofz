<?php

abstract class Foo {
    abstract public function __construct();
}

class Bar extends Foo {
    protected function __construct(){}
}