<?php

class Foo
{
    private static $bar = 123;

    static function test(){
        return function(){
            return function(){
                return Foo::$bar;
            };
        };
    }
}


$f = Foo::test();

var_dump($f()());

class A{}
$a = new A;
var_dump($f->bindTo($a, A::CLASS)()());

?>