<?php
var_dump(new class(1, 2.2, true, ["four"], new stdClass) {
    public int $int;
    public float $float;
    public bool $bool;
    public array $array;
    public stdClass $std;
    public iterable $it;

    public function __construct(int $int, float $float, bool $bool, array $array, stdClass $std) {
        $this->int = $int;
        $this->float = $float;
        $this->bool = $bool;
        $this->array = $array;
        $this->std = $std;
        $this->it = $array;
    }
});
?>