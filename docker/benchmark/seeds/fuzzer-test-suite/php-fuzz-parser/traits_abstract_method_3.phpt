<?php

trait T {
    abstract private function neededByTheTrait(int $a, string $b);
}

class C {
    use T;

    private function neededByTheTrait(array $a, object $b) {}
}

?>