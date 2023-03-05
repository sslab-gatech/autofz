<?php

class Point {
    public function __construct(
        public float $x = 0.0,
        public float $y = 1.0,
        public float $z = 2.0
    ) {}
}

var_dump(new Point(10.0));
var_dump(new Point(10.0, 11.0));
var_dump(new Point(10.0, 11.0, 12.0));

?>