def risk_score(economic, political, social):
    # Weighted scoring model
    score = (0.4 * economic) + (0.35 * political) + (0.25 * social)

    # Risk classification
    if score < 40:
        level = "Low Risk"
    elif score < 70:
        level = "Medium Risk"
    else:
        level = "High Risk"

    return round(score, 2), level


# Example run
if __name__ == "__main__":
    print("=== GDSN-X Decision Engine ===")
    
    economic = float(input("Enter Economic Risk (0-100): "))
    political = float(input("Enter Political Risk (0-100): "))
    social = float(input("Enter Social Risk (0-100): "))
    
    score, level = risk_score(economic, political, social)

    print("\nResult:")
    print("Risk Score:", score)
    print("Risk Level:", level)
