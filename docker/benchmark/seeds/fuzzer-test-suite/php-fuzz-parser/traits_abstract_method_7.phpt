<?php

trait T {
    abstract private function method(int $a, string $b);
}

abstract class C {
    use T;

    abstract protected function method(int $a, string $b);
}

class D extends C {
    protected function method(int $a, string $b) {}
}

?>
===DONE===