<?php
try {
    foreach (["test"] as $k => func()[]) {}
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
?>