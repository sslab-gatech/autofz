<?php

class T {
    public function __get($k)
    {
        return $undefined->$k;
    }

    public function __set($k, $v)
    {
        return $this->$v /= 0;
    }
}

$x = new T;
$x->x = 1;
?>