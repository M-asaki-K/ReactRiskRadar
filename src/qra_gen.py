from .utils.GPT import json_generate
from .utils.prompt import prompt_ask_for_reason_mixture_p,prompt_predict_value,mask_target_value
def generate_reason_and_predict(name,value,
                                qa_gen_command,
                                predict_command,
                                llm_ask_func=json_generate,
                                smiles="",
                                gen_reason=True,
                                n_trials=1):
    """
    Generate reason from Q&A and predict value from Q&A.
    """
    record={
        "name":name,
        "value":value,
        "smiles":smiles,
    }

    prompt=prompt_ask_for_reason(name=record['name'],value=record["value"],
                        smiles=record['smiles'],command=qa_gen_command)

    if gen_reason:
        #generate reason
        res=llm_ask_func(prompt=prompt)
        reason=mask_target_value(res["Reason"],record["value"])
    else:
        reason=""

    #predict value with reason
    prompt=prompt_predict_value(name=record['name'],reason=reason,
                                smiles=record['smiles'],command=predict_command)

    #try multiple times
    value_list=[]
    for _ in range(n_trials):
        res=llm_ask_func(prompt=prompt)
        value_list.append(res["Value"])

    record["generated_reason"]=reason
    record["predicted_values"]=value_list

    return record

from .utils.GPT import json_generate
from .utils.prompt import prompt_ask_for_reason_mixture, prompt_predict_result, mask_target_result

#混合混触危険性予測に対応
def generate_reason_and_predict_mixture(substance1, substance2, result,
                                qa_gen_command,
                                predict_command,
                                llm_ask_func=json_generate,
                                gen_reason=True,
                                n_trials=1):
    """
    Generate reason from Q&A and predict compatibility or reactivity result of a mixture.
    """
    record = {
        "substance1": substance1,
        "substance2": substance2,
        "result": result,
    }

    prompt = prompt_ask_for_reason_mixture(substance1=record['substance1'], substance2=record["substance2"],
                                   result=record["result"], command=qa_gen_command)

    if gen_reason:
        # Generate reason
        res = llm_ask_func(prompt=prompt)
        reason = mask_target_result(res["Reason"], record["result"])
    else:
        reason = ""

    # Predict result with reason
    prompt = prompt_predict_result(substance1=record['substance1'], substance2=record['substance2'],
                                   reason=reason, command=predict_command)

    # Try multiple times
    result_list = []
    for _ in range(n_trials):
        res = llm_ask_func(prompt=prompt)
        print(res)
        result_list.append(res["Result"])

    record["generated_reason"] = reason
    record["predicted_results"] = result_list

    return record

#混合混触危険性予測用、CRWのreference dataを用いて理由生成を行う場合
def generate_reason_and_predict_mixture_p(substance1, substance2, result,
                                        qa_gen_command, predict_command,
                                        llm_ask_func, reason_provided=None, gen_reason = False,
                                        n_trials=1):
    """
    Use provided Reason information to generate a reason and predict the compatibility or reactivity of a mixture.
    """
    record = {
        "substance1": substance1,
        "substance2": substance2,
        "result": result,
    }
    
    # 提供されたReasonに基づいてプロンプトを生成
    prompt = prompt_ask_for_reason_mixture_p(substance1=record['substance1'],
                                           substance2=record["substance2"],
                                           result=record["result"],
                                           command=qa_gen_command,
                                           reason_provided=reason_provided)

    if gen_reason:
        # Generate reason
        res = llm_ask_func(prompt=prompt)
        
        reason = mask_target_result(res["Reason"], record["result"])
    else:
        reason = ""

    # Predict result with reason
    prompt = prompt_predict_result(substance1=record['substance1'], substance2=record['substance2'],
                                   reason=reason, command=predict_command)

    # Try multiple times
    result_list = []
    for _ in range(n_trials):
        res = llm_ask_func(prompt=prompt)
        print(res)
        result_list.append(res["Result"])

    record["generated_reason"] = reason
    record["predicted_results"] = result_list

    return record

