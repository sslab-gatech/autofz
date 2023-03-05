<?php

trait T1 {
    abstract public function test();
}
trait T2 {
    abstract public function test(): int;
}

class C {
    use T1, T2;

    public function test(): int {}
}

?>
===DONE===