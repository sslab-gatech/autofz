<?php
class Dummy {}

new class(new Dummy) {
    public stdClass $std;

    public function __construct(Dummy $dummy) {
        $this->std = $dummy;
    }
};
?>