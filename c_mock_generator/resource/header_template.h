typedef struct <<<identifier>>>_thens <<<identifier>>>_thens_t;

<<<FORALL parameters>>>
<<<IF is_output>>>
typedef <<<method_identifier>>>_thens_t * (*<<<method_identifier>>>_then_provide_<<<identifier>>>_func)(<<<type>>>, size_t);
typedef <<<method_identifier>>>_then_provide_<<<identifier>>>_func <<<method_identifier>>>_then_provide_<<<identifier>>>_func_t;
<<<ENDIF>>>
<<<ENDFORALL>>>
typedef void (*<<<identifier>>>_then_return_func)(<<<return_type>>>);
typedef <<<identifier>>>_then_return_func <<<identifier>>>_then_return_func_t;

struct <<<identifier>>>_thens {
    <<<FORALL parameters>>>
    <<<IF is_output>>>
    <<<method_identifier>>>_then_provide_<<<identifier>>>_func_t then_provide_<<<identifier>>>;
    <<<ENDIF>>>
    <<<ENDFORALL>>>
    <<<identifier>>>_then_return_func_t then_return;
};

<<<IF has_input_parameters>>>
<<<identifier>>>_thens_t * when_<<<identifier>>>(
    <<<FORALL parameters JOINING , >>>
    <<<IF is_input>>>
    <<<type>>> <<<identifier>>>
    <<<ENDIF>>>
    <<<ENDFORALL>>>
    );
<<<ENDIF>>>
<<<IF has_no_input_parameters>>>
<<<identifier>>>_thens_t * when_<<<identifier>>>(void);
<<<ENDIF>>>

<<<IF has_parameters>>>
<<<return_type>>> <<<identifier>>>(
    <<<FORALL parameters JOINING , >>>
    <<<type>>> <<<identifier>>>
    <<<ENDFORALL>>>
    );
<<<ENDIF>>>
<<<IF has_no_parameters>>>
<<<return_type>>> <<<identifier>>>(void);
<<<ENDIF>>>
