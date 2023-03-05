<?php

trait T {
    abstract private function method(self $x): self;
}

class C {
    use T;

    private function method(int $x): int { }
}

?>
===DONE===