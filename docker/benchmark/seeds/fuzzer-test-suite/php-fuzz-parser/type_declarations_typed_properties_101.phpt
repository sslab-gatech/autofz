<?php

class Test {
    public bool $public;
    protected float $protected;
    private string $private;

    public function dump() {
        var_dump($this);
        debug_zval_dump($this);
    }
}

$test = new Test;
$test->dump();

?>