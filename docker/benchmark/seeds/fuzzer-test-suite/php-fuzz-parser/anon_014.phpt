<?php
trait TaskTrait {
    function run() {
        return 'Running...';
    }
}
$class = new class() {
  use TaskTrait;
};
var_dump($class->run());
?>