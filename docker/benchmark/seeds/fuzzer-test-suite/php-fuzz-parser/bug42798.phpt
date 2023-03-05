<?php
spl_autoload_register(function ($className) {
    print "$className\n";
    exit();
});

function foo($c = ok::constant) {
}

foo();