<?php

abstract class A
{
    abstract public function createApp();
}

class B extends A
{
    use C;
}

trait C
{
    public static function createApp()
    {
        echo "You should not be here\n";
    }
}

B::createApp();

?>