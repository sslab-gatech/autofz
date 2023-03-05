<?php

try {
    try {
        throw new Exception("Test");
    } catch (Exception $e) {
        throw $e;
    } finally {
        throw $e;
    }
} catch (Exception $e2) {
    echo $e2->getMessage(), "\n";
}

?>