from openai import OpenAI
import json
import os
from tqdm import tqdm
import re
import logging


def evaluate_document_support(openai_client, document, claim, question, model):
    """Evaluate whether a document supports, refutes, is inconclusive, or irrelevant to a specific claim."""
    evaluation_prompt = f"""# Document-Claim Conflict Detection
You are a careful fact-checking assistant specializing in identifying conflicts between claims and evidence in documents.

Decide one of the following labels for how the document relates to the claim, with respect to the question being asked:
1. SUPPORTS – The document provides evidence that directly answers the question AND supports the claim. This includes partial support - if a claim contains hedged statements or balanced perspectives (e.g., "Coffee consumption can improve alertness but may also cause sleep disruption in some individuals"), then documents that support any part of that claim should be labeled as SUPPORTS.
2. CONTRADICTS – The document provides evidence that directly answers the question BUT contradicts the claim. This includes cases where the document gives a DIFFERENT answer to the same question that is incompatible with the claim (e.g., different profession/role, different date/location/quantity/polarity/name), even if it does not explicitly say the claim is false.
3. IRRELEVANT – Either the document does not attempt to answer the question at all (no statement bearing on the specific attribute asked by the question), or it discusses the same key entities/topic but does not provide enough information to conclusively support or contradict the claim.

Decision rules:
- First ask: does the document attempt to answer the question? “Attempts” means it asserts a value for the same attribute the question asks (who/what/when/where/how many/etc.).
- If the document provides a different answer that is not matching the claim, choose CONTRADICTS (do NOT choose IRRELEVANT).
- If the document provides a matching answer OR partial support for any part of a hedged claim, choose SUPPORTS.
- If the document does not attempt to answer the question, or it is related but insufficient/uncertain, choose IRRELEVANT.
- If both supporting and contradicting statements appear, choose CONTRADICTS.

Example (contradiction via incompatible attribute):
- Question: "Who was Frédéric Chopin?"
- Claim: "Frédéric Chopin was a famous musician."
- Document: "Polish scientists born in Warsaw include … Frédéric Chopin."
- Label: CONTRADICTS (The document attempts to answer “who” by assigning a conflicting profession.)

Now evaluate the following:

# Question
{question}

# Claim to evaluate
{claim}

# Document to evaluate against
{document}

# Output format
Return ONLY a single JSON object with these fields:
{{
  "claim": "{claim}",
  "document_snippet": "<the most relevant snippet from the document that relates to the claim>",
  "reasoning": "<a brief justification that explains your decision>",
    "answer": "<SUPPORTS|CONTRADICTS|IRRELEVANT>"
}}

Please be precise and follow the decision rules. Do not include any additional text or explanations and only output in the json format specified above.
"""

    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": evaluation_prompt}],
            max_completion_tokens=4096,
            temperature=0
        )

        result = response.choices[0].message.content.strip()
        return result

    except Exception as e:
        # Local transport patch: stdout is reserved for the JSONL API.
        logging.getLogger(__name__).warning("Document support evaluation failed (%s)", type(e).__name__)
        return "<answer>ERROR</answer>"



if __name__ == "__main__":
    # Load preprocessed data
    with open("data/compiled_data_preprocessed.json", "r") as f:
        data = json.load(f)
    print(f"Loaded {len(data)} preprocessed items")

    # Initialize OpenAI client once
    model = os.environ.get("OPENAI_MODEL", "gpt-4.1")
    openai_client = OpenAI()

    processed_data = []

    for each in tqdm(data, desc="Processing entries"):
        item = each.copy()  # Make a copy to avoid modifying the original

        # Use the preprocessed claim from the data
        claim = each.get("claim", "")
        question = each["query"]

        if not claim:
            print(f"Skipping item: No claim found")
            continue

        # Evaluate the single claim against all documents
        claim_support_count = 0
        claim_not_support_count = 0
        claim_irrelevant_count = 0
        document_results = []

        # Evaluate each document against this claim
        for doc_idx, document in enumerate(each["documents"]):
            evaluation = evaluate_document_support(openai_client, document, claim, question, model)

            # Extract result - try JSON format first, then fall back to XML tags
            result = "IRRELEVANT"

            # Try to parse as JSON first
            try:
                # Look for JSON object in the response
                json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', evaluation, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    parsed_json = json.loads(json_str)
                    if "answer" in parsed_json:
                        result = parsed_json["answer"].strip().upper()
                    elif "support" in parsed_json:  # Backward compatibility
                        result = parsed_json["support"].strip().upper()
            except (json.JSONDecodeError, KeyError, AttributeError):
                # If JSON parsing fails, try regex extraction as fallback
                try:
                    json_match = re.search(r'"answer":\s*"([^"]+)"', evaluation, re.DOTALL | re.IGNORECASE)
                    if json_match:
                        result = json_match.group(1).strip().upper()
                    else:
                        # Try the old "support" field for backward compatibility
                        json_match = re.search(r'"support":\s*"([^"]+)"', evaluation, re.DOTALL | re.IGNORECASE)
                        if json_match:
                            result = json_match.group(1).strip().upper()
                except:
                    print("Error Parsing JSON:", evaluation)
                    pass

            # If JSON parsing completely fails, fall back to XML format
            if result == "IRRELEVANT":
                try:
                    match = re.search(r"<answer>(.*?)</answer>", evaluation, re.DOTALL)
                    if match:
                        result = match.group(1).strip().upper()
                except:
                    pass

            document_results.append({
                "document_index": doc_idx,
                "evaluation": result,
                "full_response": evaluation
            })

            if result == "SUPPORTS":
                claim_support_count += 1
            elif result == "CONTRADICTS":
                claim_not_support_count += 1
            else:  # INCONCLUSIVE or IRRELEVANT
                claim_irrelevant_count += 1

        # Calculate claim score
        if claim_support_count == 0 and claim_not_support_count == 0:
            claim_score = 0.0
            conflict = "IRRELEVANT"
        else:
            claim_score = claim_support_count / (claim_support_count + claim_not_support_count)
            if claim_score==1.0:
                conflict = "No"
            else:
                conflict = "Yes"

        # Store evaluation details
        claim_evaluation = {
            "claim": claim,
            "support_count": claim_support_count,
            "not_support_count": claim_not_support_count,
            "irrelevant_count": claim_irrelevant_count,
            "claim_score": claim_score,
            "document_results": document_results,
            "conflict": conflict
        }
        # Store results in the item
        item["eval_claim"] = claim_score
        item["selected_claim"] = claim
        item["eval_claim_details"] = claim_evaluation
        processed_data.append(item)

        # Save intermediate results every 10 items
        if processed_data and len(processed_data) >= 10 and len(processed_data) % 10 == 0:
            with open("outputs/calibration_evaluation_results.json", "w") as f:
                json.dump(processed_data, f, indent=4)

            print(f"Processed {len(processed_data)} items.")

    # Final save
    with open("outputs/calibration_evaluation_results.json", "w") as f:
        json.dump(processed_data, f, indent=4)

    print(f"Evaluation completed. Results saved to outputs/calibration_evaluation_results.json")
    print(f"Total processed items: {len(processed_data)}")
