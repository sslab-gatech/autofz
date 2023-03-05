<?php

const FOO = "foo";
class Bar { const FOO = "foo"; }

try {
    FOO->length();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

try {
    Bar::FOO->length();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>