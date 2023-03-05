<?php

trait T {
    abstract static public function method(int $a, string $b);
}

class C {
    use T;

    public function method(int $a, string $b) {}
}

?>