<?php
class Foo {
    public int $int = 1;
    public float $flt = 2.2;
    public float $flt2 = 2;
    public array $arr = [];
    public bool $bool = false;
    public iterable $iter = [];
}
var_dump(new Foo);
?>