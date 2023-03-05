<?php

trait T {
    abstract private function method(int $a, string $b);
}

abstract class C {
    use T;
}

class D extends C {
    private function method(int $a, string $b) {}
}

?>