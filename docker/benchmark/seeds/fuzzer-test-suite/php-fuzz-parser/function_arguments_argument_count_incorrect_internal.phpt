<?php
try {
    substr("foo");
} catch (ArgumentCountError $e) {
    echo $e->getMessage(), "\n";
}