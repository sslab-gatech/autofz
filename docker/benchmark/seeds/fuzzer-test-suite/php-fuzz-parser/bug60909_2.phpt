<?php
register_shutdown_function(function(){echo("\n\n!!!shutdown!!!\n\n");});

class Bad {
    public function __toString() {
        throw new Exception('I CAN DO THIS');
    }
}

$bad = new Bad();
echo "$bad";