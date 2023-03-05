<?php

class One {
    public function a(object $obj) {}
}

$one = new One();
$one->a(new One());
$one->a(123);