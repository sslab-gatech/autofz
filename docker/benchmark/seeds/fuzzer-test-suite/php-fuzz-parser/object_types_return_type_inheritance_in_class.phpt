<?php

class One {
    public function a() {}
}

class Two extends One {
    public function a() : object {}
}

$three = new class extends Two {
    public function a() : object {
        return 12345;
    }
};
$three->a();