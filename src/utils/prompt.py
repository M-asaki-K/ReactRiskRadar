default_ask_command="""
Provide the quantitative reasons within 300 words so that a scientist, who does not know the melting point, can predict the value.
We must quantitatively consider how the melting point shifts.
I absolutely forbid you to make qualitative generalizations.

#Bad example reasons
## Its molecular weight compared to simpler aromatic compounds, contributing to a higher melting point. (qualitative discussion is practically meaningless!!!)
## Therefore, the compound has a melting point of 110°C (Never include the answer in the reason!!).

#Good example reasons
## Benzene has a boiling point of 80 degrees, but toluene with a methyl group improves the boiling point by about +30 degrees due to its larger molecular weight and other reasons (+30 contribution).
## Butane has a boiling point of -1°C, but butanol with a hydroxy group has a boiling point increase of about 115°C due to the strong influence of hydrogen bonding (+115 contribution).

#Output: Reason key
"""

default_predict_command="""
Predict the melting point of the following compound.
In any case, output some value.

#Output: Value key
"""

default_ask_command_mixture = """
Provide the quantitative reasons within 300 words so that a scientist, who does not know the compatibility or reactivity results of a mixture, can predict these outcomes.
We must quantitatively consider how the combination of substances influences the compatibility or reactivity.
I absolutely forbid you to make qualitative generalizations.

#Bad example reasons
## Its molecular weight compared to simpler compounds, contributing to a higher reactivity. (qualitative discussion is practically meaningless!!!)
## Therefore, the mixture is highly reactive. (Never include the answer in the reason!!).

#Good example reasons
## Sodium reacts vigorously with water, generating a significant amount of heat and hydrogen gas, which can lead to an explosive reaction under certain conditions.
## Acetone and bleach mixture creates chloroform and other hazardous compounds due to the chemical reaction between acetone's methyl groups and sodium hypochlorite in bleach.

#Output: Reason key
"""

default_predict_command_mixture = """
Predict the compatibility or reactivity of the following mixture.
Consider the quantitative reasons provided and, in any case, output a prediction about the mixture's safety or potential hazards.

#Output: Prediction key
"""


# prompt to generate "reason" from Q&A
def prompt_ask_for_reason(name,value,smiles="",command=default_ask_command):
    prompt=command

    prompt+=f"""
Name: {name}"""

    if smiles!="":
        prompt+=f"""
SMILES: {smiles}"""

    prompt+=f"""
Value: {value}
Reason: """

    return prompt.strip()

# predict value from Q( and reason)
def prompt_predict_value(name,reason="",smiles="",command=default_predict_command):
    prompt=command

    prompt+=f"""
Name: {name}"""

    if smiles!="":
        prompt+=f"""
SMILES: {smiles}"""

    if reason!="":
        prompt+=f"""
Reason: {reason}"""
    
        prompt+=f"""
Value: """
            
    return prompt.strip()


#mask target value in the reason text, if included
def mask_target_value(reason,value):
    reason=reason.replace(str(value),"[MASK]")
    return reason

#混合混触に対応した書き換え版
def prompt_ask_for_reason_mixture(substance1, substance2, result, command=default_ask_command_mixture):
    prompt = command

    prompt += f"""
Substance 1: {substance1}
Substance 2: {substance2}"""

    prompt += f"""
Result: {result}
Reason: """

    return prompt.strip()

def prompt_ask_for_reason_mixture_p(substance1, substance2, result, command, reason_provided=None):
    prompt = command

    prompt += f"""
Substance 1: {substance1}
Substance 2: {substance2}"""

    # 提供されたReasonがある場合、それをプロンプトに含める
    if reason_provided:
        prompt += f"""
Result: {result}
Reference: {reason_provided}
Reason: """
    else:
        # Reasonが提供されていない場合は、Result情報のみを含める
        prompt += f"""
Result: {result}
Reason: """

    return prompt.strip()


def prompt_predict_result(substance1, substance2, reason="", command=default_predict_command_mixture):
    prompt = command

    prompt += f"""
Substance 1: {substance1}
Substance 2: {substance2}"""

    if reason != "":
        prompt += f"""
Reason: {reason}"""
    
    prompt += f"""
Result: """
            
    return prompt.strip()

def mask_target_result(reason, result):
    masked_reason = reason.replace(result, "[MASK]")
    return masked_reason
