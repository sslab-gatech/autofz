<?php
declare(strict_types=1);

class Bar
{
    public float $bar;

    public function setBar($value) {
        $this->bar = $value;
    }
}

$bar = new Bar();

$bar->setBar(100);

var_dump($bar->bar);