import re
from typing import Dict, Any, List, Tuple
import structlog

logger = structlog.get_logger(__name__)


class SafetyEngine:
    """
    Multi-layer safety and compliance checking engine
    Handles: PII detection, injection detection, toxicity, jailbreak
    """

    # PII Patterns
    PII_PATTERNS = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone_us": r"\b(\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
        "ssn": r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b",
        "credit_card": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        "ip_address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "date_of_birth": r"\b(0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])[-/](19|20)\d{2}\b",
        "passport": r"\b[A-Z]{1,2}\d{6,9}\b",
        "drivers_license": r"\b[A-Z]{1,2}\d{5,8}\b",
        "medical_record": r"\b(MRN|MR#|Medical Record)\s*:?\s*\d+\b",
        "bank_account": r"\b\d{8,17}\b",
    }

    # Injection Attack Patterns  
    INJECTION_PATTERNS = [
        r"ignore (previous|all|above) instructions",
        r"disregard (your|the) (system|previous) (prompt|instructions)",
        r"you are now (a|an) (different|new|unrestricted)",
        r"jailbreak",
        r"dan mode",
        r"developer mode",
        r"(bypass|override) (your|the) (safety|restrictions|guidelines)",
        r"pretend (you have no|you don't have) restrictions",
        r"act as if you were (trained|programmed) differently",
        r"forget (your|all) (training|instructions|guidelines)",
        r"new persona",
        r"roleplaying as (an|a) ai without",
    ]

    # High-Risk Keywords
    HIGH_RISK_KEYWORDS = [
        "bomb making", "weapon synthesis", "drug synthesis",
        "hack into", "exploit vulnerability", "ransomware",
        "child", "minor", "illegal content", "terrorism",
    ]

    def analyze(self, content: str) -> Dict[str, Any]:
        results = {
            "is_safe": True,
            "safety_score": 1.0,
            "pii_detected": [],
            "injection_risk": False,
            "injection_patterns": [],
            "high_risk_content": False,
            "high_risk_keywords": [],
            "toxicity_indicators": [],
            "compliance_flags": [],
            "recommendations": [],
            "masked_content": content,
        }

        # PII Detection
        pii_found, masked = self._detect_and_mask_pii(content)
        results["pii_detected"] = pii_found
        results["masked_content"] = masked
        if pii_found:
            results["safety_score"] -= 0.2
            results["compliance_flags"].append("PII_DETECTED")
            results["recommendations"].append(
                f"PII detected: {', '.join(pii_found)}. Consider masking sensitive data."
            )

        # Injection Detection
        injection_found = self._detect_injection(content)
        if injection_found:
            results["injection_risk"] = True
            results["injection_patterns"] = injection_found
            results["is_safe"] = False
            results["safety_score"] -= 0.5
            results["compliance_flags"].append("INJECTION_ATTEMPT")
            results["recommendations"].append(
                "Potential prompt injection detected. Review and sanitize input."
            )

        # High Risk Content
        risk_keywords = self._detect_high_risk(content)
        if risk_keywords:
            results["high_risk_content"] = True
            results["high_risk_keywords"] = risk_keywords
            results["is_safe"] = False
            results["safety_score"] -= 0.4
            results["compliance_flags"].append("HIGH_RISK_CONTENT")

        # Final score normalization
        results["safety_score"] = max(0.0, min(1.0, results["safety_score"]))

        logger.info(
            "Safety analysis completed",
            is_safe=results["is_safe"],
            safety_score=results["safety_score"],
            pii_count=len(results["pii_detected"]),
        )

        return results

    def _detect_and_mask_pii(self, content: str) -> Tuple[List[str], str]:
        detected = []
        masked = content
        
        for pii_type, pattern in self.PII_PATTERNS.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                detected.append(pii_type)
                masked = re.sub(
                    pattern,
                    f"[{pii_type.upper()}_REDACTED]",
                    masked,
                    flags=re.IGNORECASE,
                )
        return detected, masked

    def _detect_injection(self, content: str) -> List[str]:
        content_lower = content.lower()
        found = []
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, content_lower, re.IGNORECASE):
                found.append(pattern)
        return found

    def _detect_high_risk(self, content: str) -> List[str]:
        content_lower = content.lower()
        return [kw for kw in self.HIGH_RISK_KEYWORDS if kw in content_lower]


safety_engine = SafetyEngine()