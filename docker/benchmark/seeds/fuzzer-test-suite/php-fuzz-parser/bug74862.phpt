<?php

class a {
    private function __clone()
    {

    }

    private function __construct()
    {

    }

    public static function getInstance()
    {
        return new static();
    }

    public function cloneIt()
    {
        $a = clone $this;

        return $a;
    }
}

class c extends a {

}

// private constructor
$d = c::getInstance();

// private clone
$e = $d->cloneIt();
var_dump($e);
?>