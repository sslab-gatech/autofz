<?php
assert(0 && ($a = function (int $a, ?int $b, int $c = null): ?int {
    $x = new class {
        public $a;
        public int $b;
        public ?int $c;
    };
}));
?>