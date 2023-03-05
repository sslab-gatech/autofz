<?php

interface RootInterface
{
    function foo();
}

interface FirstChildInterface extends RootInterface
{
    function foo();
}

interface SecondChildInterface extends RootInterface
{
    function foo();
}

class A implements FirstChildInterface, SecondChildInterface
{
    function foo()
    {
    }
}

class B implements RootInterface, FirstChildInterface
{
    function foo()
    {
    }
}

class C implements FirstChildInterface, RootInterface
{
    function foo()
    {
    }
}

?>
===DONE===