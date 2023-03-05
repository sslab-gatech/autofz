<?php

trait T {
    abstract public function neededByTheTrait(int $a, string $b);
}

class C {
    use T;

    public function neededByTheTrait(array $a, object $b) {}
}

?>