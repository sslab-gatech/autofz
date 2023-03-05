<?php
$thing = new class() {
    public int $int;
};

$var = &$thing->int;
?>