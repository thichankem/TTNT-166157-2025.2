"""
Knowledge base: 100 diseases x ~300 symptoms
Vietnamese keyword mappings for NLP symptom extraction (Model 1)
"""

# ─────────────────────────── SYMPTOM CODES (~300) ─────────────────────────── #
SYMPTOMS_LIST = [
    # ── General (20) ──────────────────────────────────────────────────────────
    "fever", "high_fever", "low_grade_fever", "chills", "sweating",
    "night_sweats", "fatigue", "weakness", "malaise", "weight_loss",
    "weight_gain", "loss_of_appetite", "increased_appetite", "dehydration",
    "body_aches", "pallor", "jaundice", "cyanosis", "swollen_lymph_nodes",
    "recurrent_infections",

    # ── Neurological (32) ─────────────────────────────────────────────────────
    "headache", "severe_headache", "dizziness", "vertigo", "confusion",
    "memory_loss", "difficulty_concentrating", "seizures", "tremors",
    "numbness", "tingling", "fainting", "loss_of_consciousness", "insomnia",
    "excessive_sleepiness", "mood_changes", "irritability", "hallucinations",
    "paralysis", "weakness_one_side", "speech_difficulty", "vision_changes",
    "double_vision", "slow_movements", "shuffling_gait", "pill_rolling_tremor",
    "mask_face", "stooped_posture", "cognitive_decline", "personality_changes",
    "agitation", "word_finding_difficulty",

    # ── Eyes (13) ─────────────────────────────────────────────────────────────
    "eye_pain", "red_eyes", "eye_discharge", "blurred_vision",
    "light_sensitivity", "eye_itching", "swollen_eyelids", "floaters",
    "tunnel_vision", "eye_pressure", "gradual_vision_loss",
    "sudden_vision_loss", "halos_around_lights",

    # ── ENT (15) ──────────────────────────────────────────────────────────────
    "ear_pain", "ear_discharge", "hearing_loss", "tinnitus",
    "nasal_congestion", "runny_nose", "sneezing", "loss_of_smell",
    "nosebleed", "sore_throat", "difficulty_swallowing", "hoarseness",
    "throat_irritation", "throat_swelling", "parotid_swelling",

    # ── Respiratory (21) ──────────────────────────────────────────────────────
    "cough", "dry_cough", "productive_cough", "coughing_blood",
    "shortness_of_breath", "wheezing", "rapid_breathing", "chest_tightness",
    "chest_pain", "barrel_chest", "pursed_lip_breathing",
    "decreased_breath_sounds", "crackles", "rhonchi", "stridor",
    "hemoptysis", "chronic_cough", "sputum_production",
    "accessory_muscle_use", "exertional_dyspnea", "pleuritic_chest_pain",

    # ── Cardiovascular (18) ───────────────────────────────────────────────────
    "palpitations", "irregular_heartbeat", "rapid_heart_rate",
    "slow_heart_rate", "high_blood_pressure", "low_blood_pressure",
    "leg_swelling", "cold_extremities", "cyanosis_extremities", "orthopnea",
    "pedal_edema", "pink_frothy_sputum", "chest_pressure",
    "fainting_on_exertion", "calf_pain", "jaw_pain", "arm_pain",
    "neck_vein_distension",

    # ── Gastrointestinal (26) ─────────────────────────────────────────────────
    "nausea", "vomiting", "abdominal_pain", "upper_abdominal_pain",
    "lower_abdominal_pain", "right_lower_abdominal_pain", "stomach_cramps",
    "bloating", "gas", "diarrhea", "constipation", "bloody_stool",
    "dark_stool", "mucus_in_stool", "heartburn", "acid_reflux",
    "indigestion", "abdominal_distension", "rectal_bleeding",
    "pain_after_eating", "pain_relieved_by_eating", "jaundice_skin",
    "liver_tenderness", "ascites", "clay_colored_stool", "rice_water_stool",

    # ── Urinary (13) ──────────────────────────────────────────────────────────
    "frequent_urination", "painful_urination", "burning_urination",
    "difficulty_urinating", "blood_in_urine", "cloudy_urine", "dark_urine",
    "urinary_incontinence", "nocturia", "decreased_urine_output",
    "kidney_pain", "flank_pain", "pelvic_pain",

    # ── Musculoskeletal (20) ──────────────────────────────────────────────────
    "joint_pain", "joint_swelling", "joint_stiffness", "morning_stiffness",
    "muscle_pain", "muscle_weakness", "muscle_cramps", "back_pain",
    "lower_back_pain", "neck_pain", "neck_stiffness", "shoulder_pain",
    "knee_pain", "hip_pain", "bone_pain", "reduced_range_of_motion",
    "balance_problems", "foot_pain", "gait_disturbance", "tophi",

    # ── Skin (26) ─────────────────────────────────────────────────────────────
    "rash", "skin_redness", "itching", "hives", "blisters", "skin_lesions",
    "peeling_skin", "dry_skin", "acne", "blackheads", "pustules",
    "skin_thickening", "skin_discoloration", "bruising", "petechiae",
    "purpura", "hair_loss", "nail_changes", "skin_ulcer",
    "wounds_not_healing", "butterfly_rash", "photosensitivity_skin",
    "maculopapular_rash", "vesicular_rash", "spotted_rash",
    "acanthosis_nigricans",

    # ── Reproductive / Hormonal (22) ──────────────────────────────────────────
    "irregular_menstruation", "heavy_menstrual_bleeding",
    "painful_menstruation", "absent_menstruation", "vaginal_discharge",
    "vaginal_bleeding", "breast_pain", "breast_lump", "nipple_discharge",
    "erectile_dysfunction", "testicular_pain", "testicular_swelling",
    "penile_discharge", "increased_thirst", "excessive_hunger",
    "heat_intolerance", "cold_intolerance", "goiter", "hot_flashes",
    "cold_sensitivity", "exophthalmos", "rapid_pulse",

    # ── Mental-health signals (12) ────────────────────────────────────────────
    "low_mood", "hopelessness", "panic_attacks", "excessive_worry",
    "sleep_disturbance", "appetite_changes", "loss_of_interest",
    "social_withdrawal", "aura", "phonophobia", "migraine_headache",
    "nausea_with_headache",

    # ── Metabolic / Immune / Other (30) ───────────────────────────────────────
    "high_cholesterol", "obesity", "slow_wound_healing",
    "easy_bruising", "prolonged_bleeding", "lump_or_mass",
    "unexplained_weight_loss", "fatigue_cancer", "enlarged_liver",
    "enlarged_spleen", "pleuritis", "pericarditis", "proteinuria",
    "fine_tremor", "bradycardia", "puffy_face", "coarse_hair",
    "dry_coarse_skin", "genital_lesions", "koplik_spots",
    "spastic_paralysis", "optic_neuritis", "facial_pain", "facial_palsy",
    "jaw_stiffness", "risus_sardonicus", "opisthotonus", "kaposi_sarcoma",
    "oral_thrush", "rose_spots",
]

# ─────────────────── VIETNAMESE KEYWORD → SYMPTOM CODE ───────────────────── #
# Each symptom maps to a list of Vietnamese / English keywords.
# process_clinical_text() scans user text for these keywords.
SYMPTOM_KEYWORDS: dict[str, list[str]] = {
    "fever": [
        "sốt", "bị sốt", "nóng người", "thân nhiệt tăng", "sốt nhẹ",
        "ấm đầu", "fever", "temperature"],
    "high_fever": [
        "sốt cao", "sốt rất cao", "sốt 39", "sốt 40", "sốt cao liên tục",
        "high fever", "sốt cao độ"],
    "low_grade_fever": [
        "sốt âm ỉ", "sốt nhẹ", "hơi sốt", "sốt 37", "sốt 38", "low grade fever"],
    "chills": [
        "ớn lạnh", "rùng mình", "lạnh run", "run lạnh", "rét run",
        "ớn gáy", "chills"],
    "sweating": [
        "đổ mồ hôi", "ra mồ hôi", "mồ hôi nhiều", "toát mồ hôi",
        "sweating", "perspiration"],
    "night_sweats": [
        "đổ mồ hôi đêm", "ra mồ hôi về đêm", "mồ hôi trộm",
        "night sweats", "đổ mồ hôi ban đêm"],
    "fatigue": [
        "mệt mỏi", "kiệt sức", "mệt", "uể oải", "người mệt",
        "fatigue", "tired", "exhausted"],
    "weakness": [
        "yếu người", "người yếu", "không có sức", "lả người",
        "weakness", "weak", "lả lướt"],
    "malaise": [
        "khó chịu", "người khó chịu", "bất ổn", "cảm thấy không tốt",
        "malaise", "unwell"],
    "weight_loss": [
        "sụt cân", "giảm cân", "gầy đi", "sút cân", "cân nặng giảm",
        "weight loss", "losing weight"],
    "weight_gain": [
        "tăng cân", "béo lên", "tăng trọng lượng", "weight gain"],
    "loss_of_appetite": [
        "chán ăn", "không muốn ăn", "mất cảm giác thèm ăn", "ăn không ngon",
        "kém ăn", "loss of appetite", "không có cảm giác đói"],
    "increased_appetite": [
        "ăn nhiều", "đói nhiều", "thèm ăn liên tục", "increased appetite"],
    "dehydration": [
        "mất nước", "khô người", "dehydration", "thiếu nước", "khát nhiều"],
    "body_aches": [
        "đau nhức người", "nhức mình", "đau toàn thân", "nhức cơ",
        "body aches", "đau nhức toàn thân"],
    "pallor": [
        "da nhợt nhạt", "mặt tái", "xanh xao", "nhợt nhạt", "pallor", "pale"],
    "jaundice": [
        "vàng da", "vàng mắt", "da vàng", "mắt vàng", "jaundice",
        "da và mắt vàng"],
    "cyanosis": [
        "tím tái", "xanh tím", "cyanosis", "môi tím", "tím môi"],
    "swollen_lymph_nodes": [
        "hạch sưng", "hạch bạch huyết sưng", "nổi hạch", "hạch to",
        "lymph nodes", "hạch cổ sưng"],
    "recurrent_infections": [
        "nhiễm trùng tái phát", "hay bị bệnh", "sức đề kháng yếu",
        "recurrent infections"],

    # Neurological
    "headache": [
        "đau đầu", "nhức đầu", "đầu nhức", "đầu đau", "headache",
        "nhức đầu dữ dội"],
    "severe_headache": [
        "đau đầu dữ dội", "đau đầu không chịu nổi", "đau đầu như búa bổ",
        "severe headache", "đau đầu rất mạnh"],
    "dizziness": [
        "chóng mặt", "hoa mắt", "quay cuồng", "choáng váng",
        "dizziness", "đầu óc quay", "váng đầu"],
    "vertigo": [
        "chóng mặt xoay", "cảm giác quay tròn", "vertigo",
        "đầu quay tròn", "chóng mặt tư thế"],
    "confusion": [
        "lú lẫn", "mất phương hướng", "không tỉnh táo", "confusion",
        "lơ mơ", "không nhận thức rõ"],
    "memory_loss": [
        "mất trí nhớ", "hay quên", "quên nhiều", "memory loss",
        "không nhớ", "trí nhớ giảm"],
    "difficulty_concentrating": [
        "khó tập trung", "không tập trung được", "mất tập trung",
        "difficulty concentrating"],
    "seizures": [
        "co giật", "động kinh", "giật toàn thân", "seizures",
        "lên cơn giật"],
    "tremors": [
        "run tay", "run chân", "run rẩy", "tremors", "run tay chân"],
    "numbness": [
        "tê liệt", "tê tay", "tê chân", "tê bì", "numbness", "tê",
        "mất cảm giác"],
    "tingling": [
        "tê ngứa", "kiến bò", "ngứa ran", "tingling", "cảm giác kiến bò"],
    "fainting": [
        "ngất xỉu", "bất tỉnh", "té xỉu", "fainting", "mất ý thức tạm thời"],
    "loss_of_consciousness": [
        "mất ý thức", "bất tỉnh nhân sự", "ngất", "loss of consciousness"],
    "insomnia": [
        "mất ngủ", "không ngủ được", "khó ngủ", "insomnia", "ngủ không được"],
    "excessive_sleepiness": [
        "ngủ nhiều", "buồn ngủ liên tục", "hypersomnia", "ngủ không thức dậy được"],
    "mood_changes": [
        "thay đổi tâm trạng", "tâm trạng thất thường", "mood changes",
        "cảm xúc không ổn định"],
    "irritability": [
        "cáu kỉnh", "dễ bực bội", "hay cáu", "irritability", "nóng tính"],
    "hallucinations": [
        "ảo giác", "nhìn thấy ảo ảnh", "nghe thấy giọng nói",
        "hallucinations"],
    "paralysis": [
        "liệt", "tê liệt", "paralysis", "không cử động được"],
    "weakness_one_side": [
        "yếu nửa người", "liệt nửa người", "yếu tay phải",
        "yếu tay trái", "weakness one side"],
    "speech_difficulty": [
        "khó nói", "nói khó", "nói không rõ", "nói lắp", "speech difficulty",
        "ngọng", "mất ngôn ngữ"],
    "vision_changes": [
        "nhìn mờ", "mờ mắt", "thay đổi thị lực", "vision changes",
        "nhìn không rõ"],
    "double_vision": [
        "nhìn đôi", "nhìn thấy hai", "double vision"],
    "slow_movements": [
        "cử động chậm", "chuyển động chậm chạp", "slow movements",
        "vận động chậm"],
    "shuffling_gait": [
        "đi lê bước", "bước đi ngắn", "đi khom", "shuffling gait"],
    "pill_rolling_tremor": [
        "run như viên thuốc", "run đặc trưng parkinson", "pill rolling tremor"],
    "mask_face": [
        "khuôn mặt vô cảm", "mặt như mặt nạ", "mask face"],
    "stooped_posture": [
        "cong người", "lưng khom", "tư thế gù", "stooped posture"],
    "cognitive_decline": [
        "suy giảm nhận thức", "trí tuệ giảm", "cognitive decline",
        "nhận thức kém"],
    "personality_changes": [
        "thay đổi tính cách", "tính tình thay đổi", "personality changes"],
    "agitation": [
        "kích động", "bất an", "agitation", "bồn chồn"],
    "word_finding_difficulty": [
        "khó tìm từ", "không tìm được từ", "word finding difficulty",
        "quên từ"],

    # Eyes
    "eye_pain": [
        "đau mắt", "nhức mắt", "eye pain"],
    "red_eyes": [
        "mắt đỏ", "mắt đỏ hoe", "mắt sung huyết", "red eyes"],
    "eye_discharge": [
        "ghèn mắt", "dịch mắt", "tiết dịch mắt", "eye discharge",
        "mắt có mủ"],
    "blurred_vision": [
        "nhìn mờ", "mắt mờ", "thị lực giảm", "blurred vision"],
    "light_sensitivity": [
        "nhạy cảm ánh sáng", "sợ ánh sáng", "photophobia",
        "nhìn sáng đau mắt"],
    "eye_itching": [
        "ngứa mắt", "mắt ngứa", "eye itching"],
    "swollen_eyelids": [
        "mi mắt sưng", "mắt sưng", "swollen eyelids"],
    "floaters": [
        "ruồi bay", "đom đóm mắt", "floaters", "thấy đốm bay"],
    "tunnel_vision": [
        "tầm nhìn hẹp", "nhìn như đường hầm", "tunnel vision"],
    "eye_pressure": [
        "áp lực mắt", "cảm giác nặng mắt", "eye pressure"],
    "gradual_vision_loss": [
        "mờ mắt từ từ", "thị lực giảm dần", "gradual vision loss"],
    "sudden_vision_loss": [
        "mất thị lực đột ngột", "mù đột ngột", "sudden vision loss"],
    "halos_around_lights": [
        "hào quang quanh đèn", "nhìn đèn thấy vòng sáng", "halos"],

    # ENT
    "ear_pain": [
        "đau tai", "nhức tai", "ear pain"],
    "ear_discharge": [
        "chảy dịch tai", "dịch tai", "ear discharge", "mủ tai"],
    "hearing_loss": [
        "giảm thính lực", "nghe kém", "điếc", "hearing loss",
        "mất thính giác"],
    "tinnitus": [
        "ù tai", "tiếng kêu trong tai", "tinnitus"],
    "nasal_congestion": [
        "nghẹt mũi", "tắc mũi", "mũi tắc", "nasal congestion",
        "không thở mũi được"],
    "runny_nose": [
        "chảy nước mũi", "sổ mũi", "nước mũi chảy", "runny nose"],
    "sneezing": [
        "hắt hơi", "hắt hơi nhiều", "sneezing"],
    "loss_of_smell": [
        "mất mùi", "không ngửi được", "anosmia", "mất khứu giác"],
    "nosebleed": [
        "chảy máu mũi", "chảy máu cam", "nosebleed"],
    "sore_throat": [
        "đau họng", "họng đau", "rát họng", "sore throat", "viêm họng"],
    "difficulty_swallowing": [
        "khó nuốt", "nuốt đau", "nuốt khó", "difficulty swallowing",
        "dysphagia"],
    "hoarseness": [
        "khàn tiếng", "giọng khàn", "mất tiếng", "hoarseness",
        "giọng khàn đặc"],
    "throat_irritation": [
        "kích ứng họng", "họng khó chịu", "ngứa họng", "throat irritation"],
    "throat_swelling": [
        "sưng họng", "cổ họng sưng", "throat swelling"],
    "parotid_swelling": [
        "sưng tuyến nước bọt", "sưng mang tai", "quai bị", "parotid swelling",
        "má sưng"],

    # Respiratory
    "cough": [
        "ho", "bị ho", "ho nhiều", "húng hắng ho", "cough"],
    "dry_cough": [
        "ho khan", "ho không đờm", "dry cough"],
    "productive_cough": [
        "ho có đờm", "ho đờm", "productive cough", "ho ra đờm"],
    "coughing_blood": [
        "ho ra máu", "khạc máu", "coughing blood", "ho máu"],
    "shortness_of_breath": [
        "khó thở", "hụt hơi", "thở không đủ hơi", "shortness of breath",
        "thở ngắn", "không thở được"],
    "wheezing": [
        "thở khò khè", "khò khè", "wheezing", "tiếng thở rít"],
    "rapid_breathing": [
        "thở nhanh", "thở gấp", "rapid breathing", "tachypnea"],
    "chest_tightness": [
        "tức ngực", "ngực tức", "chest tightness", "nặng ngực"],
    "chest_pain": [
        "đau ngực", "ngực đau", "chest pain", "tức đau ngực"],
    "barrel_chest": [
        "lồng ngực hình thùng", "ngực tròn", "barrel chest"],
    "pursed_lip_breathing": [
        "thở môi mím", "pursed lip breathing"],
    "decreased_breath_sounds": [
        "giảm âm thở", "phổi câm", "decreased breath sounds"],
    "crackles": [
        "ran ẩm", "ran nổ", "crackles", "tiếng ran phổi"],
    "rhonchi": [
        "ran ngáy", "rhonchi"],
    "stridor": [
        "thở rít thanh quản", "stridor"],
    "hemoptysis": [
        "ho ra máu", "khạc máu", "hemoptysis"],
    "chronic_cough": [
        "ho mãn tính", "ho kéo dài", "ho dai dẳng", "chronic cough"],
    "sputum_production": [
        "tiết đờm nhiều", "đờm nhiều", "sputum production"],
    "accessory_muscle_use": [
        "dùng cơ hô hấp phụ", "accessory muscle use"],
    "exertional_dyspnea": [
        "khó thở khi gắng sức", "vận động khó thở", "exertional dyspnea",
        "leo cầu thang khó thở"],
    "pleuritic_chest_pain": [
        "đau ngực kiểu màng phổi", "đau khi thở sâu", "pleuritic chest pain"],

    # Cardiovascular
    "palpitations": [
        "đánh trống ngực", "tim đập mạnh", "tim hồi hộp", "palpitations",
        "cảm thấy tim đập"],
    "irregular_heartbeat": [
        "nhịp tim không đều", "rối loạn nhịp tim", "irregular heartbeat",
        "tim đập loạn"],
    "rapid_heart_rate": [
        "tim đập nhanh", "nhịp tim nhanh", "rapid heart rate", "tachycardia"],
    "slow_heart_rate": [
        "tim đập chậm", "nhịp tim chậm", "slow heart rate", "bradycardia"],
    "high_blood_pressure": [
        "huyết áp cao", "tăng huyết áp", "áp huyết cao",
        "high blood pressure", "hypertension"],
    "low_blood_pressure": [
        "huyết áp thấp", "tụt huyết áp", "low blood pressure",
        "hypotension"],
    "leg_swelling": [
        "phù chân", "chân sưng", "leg swelling", "chân phù"],
    "cold_extremities": [
        "tay chân lạnh", "chân tay lạnh", "cold hands feet",
        "cold extremities"],
    "cyanosis_extremities": [
        "tím đầu ngón tay", "ngón tay tím", "cyanosis extremities"],
    "orthopnea": [
        "khó thở khi nằm", "nằm khó thở", "orthopnea",
        "phải ngồi để thở"],
    "pedal_edema": [
        "phù mắt cá", "phù bàn chân", "pedal edema"],
    "pink_frothy_sputum": [
        "đờm hồng bọt", "pink frothy sputum"],
    "chest_pressure": [
        "áp lực ngực", "nặng ngực", "chest pressure",
        "ngực bị đè nén"],
    "fainting_on_exertion": [
        "ngất khi gắng sức", "ngất khi vận động", "fainting on exertion"],
    "calf_pain": [
        "đau bắp chân", "bắp chân đau", "calf pain"],
    "jaw_pain": [
        "đau hàm", "hàm đau", "jaw pain"],
    "arm_pain": [
        "đau cánh tay", "tay đau", "arm pain"],
    "neck_vein_distension": [
        "tĩnh mạch cổ nổi", "tĩnh mạch cổ căng", "JVD", "neck vein distension"],

    # Gastrointestinal
    "nausea": [
        "buồn nôn", "muốn nôn", "nôn nao", "nausea"],
    "vomiting": [
        "nôn", "ói", "nôn mửa", "vomiting", "ói mửa"],
    "abdominal_pain": [
        "đau bụng", "bụng đau", "abdominal pain", "đau ở bụng"],
    "upper_abdominal_pain": [
        "đau thượng vị", "đau vùng bụng trên", "đau dạ dày",
        "upper abdominal pain", "đau vùng trên rốn"],
    "lower_abdominal_pain": [
        "đau bụng dưới", "đau vùng bụng dưới", "lower abdominal pain"],
    "right_lower_abdominal_pain": [
        "đau bụng dưới bên phải", "đau hố chậu phải",
        "right lower abdominal pain"],
    "stomach_cramps": [
        "co thắt dạ dày", "chuột rút bụng", "stomach cramps", "bụng quặn"],
    "bloating": [
        "chướng bụng", "bụng phình", "đầy bụng", "bloating",
        "bụng đầy hơi"],
    "gas": [
        "đầy hơi", "hơi bụng", "gas", "xì hơi nhiều"],
    "diarrhea": [
        "tiêu chảy", "đi ngoài nhiều lần", "phân lỏng", "diarrhea",
        "đi tiêu phân lỏng"],
    "constipation": [
        "táo bón", "không đi tiêu được", "phân cứng", "constipation",
        "khó đi vệ sinh"],
    "bloody_stool": [
        "phân có máu", "đi cầu ra máu", "bloody stool", "máu trong phân"],
    "dark_stool": [
        "phân đen", "phân có màu đen", "dark stool", "phân melena"],
    "mucus_in_stool": [
        "phân có nhầy", "nhầy trong phân", "mucus in stool"],
    "heartburn": [
        "ợ nóng", "nóng rát ngực", "heartburn", "ợ hơi nóng"],
    "acid_reflux": [
        "trào ngược axit", "acid reflux", "trào ngược dạ dày",
        "axit trào lên"],
    "indigestion": [
        "khó tiêu", "ăn không tiêu", "indigestion", "tiêu hóa kém"],
    "abdominal_distension": [
        "bụng căng phồng", "bụng to", "abdominal distension"],
    "rectal_bleeding": [
        "chảy máu hậu môn", "rectal bleeding", "máu ở hậu môn"],
    "pain_after_eating": [
        "đau sau ăn", "ăn xong đau", "pain after eating"],
    "pain_relieved_by_eating": [
        "ăn hết đau", "đau giảm khi ăn", "pain relieved by eating"],
    "jaundice_skin": [
        "vàng da", "da vàng", "jaundice skin", "da và mắt vàng"],
    "liver_tenderness": [
        "gan đau khi ấn", "đau vùng gan", "liver tenderness"],
    "ascites": [
        "cổ trướng", "bụng nước", "ascites", "bụng to chứa nước"],
    "clay_colored_stool": [
        "phân bạc màu", "phân màu đất sét", "clay colored stool"],
    "rice_water_stool": [
        "phân như nước vo gạo", "rice water stool", "phân lỏng trong"],

    # Urinary
    "frequent_urination": [
        "tiểu nhiều lần", "đi tiểu nhiều", "tiểu liên tục",
        "frequent urination", "đi vệ sinh nhiều"],
    "painful_urination": [
        "tiểu đau", "đau khi tiểu", "painful urination"],
    "burning_urination": [
        "tiểu buốt", "buốt khi tiểu", "burning urination",
        "rát khi đi tiểu"],
    "difficulty_urinating": [
        "tiểu khó", "tiểu nhỏ giọt", "difficulty urinating",
        "không tiểu được"],
    "blood_in_urine": [
        "tiểu ra máu", "nước tiểu có máu", "blood in urine",
        "đái ra máu"],
    "cloudy_urine": [
        "nước tiểu đục", "tiểu đục", "cloudy urine"],
    "dark_urine": [
        "nước tiểu sẫm màu", "nước tiểu vàng đậm", "dark urine",
        "tiểu màu nâu"],
    "urinary_incontinence": [
        "tiểu không kiểm soát", "tiểu không tự chủ", "urinary incontinence"],
    "nocturia": [
        "tiểu đêm", "đêm hay thức tiểu", "nocturia", "đi tiểu nhiều ban đêm"],
    "decreased_urine_output": [
        "tiểu ít", "giảm lượng nước tiểu", "decreased urine output",
        "nước tiểu ít"],
    "kidney_pain": [
        "đau thận", "kidney pain"],
    "flank_pain": [
        "đau hông lưng", "đau ở hông", "flank pain", "đau sườn"],
    "pelvic_pain": [
        "đau vùng chậu", "đau vùng hạ vị", "pelvic pain"],

    # Musculoskeletal
    "joint_pain": [
        "đau khớp", "khớp đau", "joint pain", "đau ở khớp"],
    "joint_swelling": [
        "sưng khớp", "khớp sưng", "joint swelling"],
    "joint_stiffness": [
        "cứng khớp", "khớp cứng", "joint stiffness"],
    "morning_stiffness": [
        "cứng khớp buổi sáng", "khớp cứng khi mới dậy",
        "morning stiffness"],
    "muscle_pain": [
        "đau cơ", "cơ đau", "muscle pain", "nhức cơ"],
    "muscle_weakness": [
        "yếu cơ", "cơ yếu", "muscle weakness"],
    "muscle_cramps": [
        "chuột rút", "vọp bẻ", "muscle cramps", "cơ co rút"],
    "back_pain": [
        "đau lưng", "lưng đau", "back pain"],
    "lower_back_pain": [
        "đau lưng dưới", "đau thắt lưng", "lower back pain"],
    "neck_pain": [
        "đau cổ", "cổ đau", "neck pain"],
    "neck_stiffness": [
        "cứng cổ", "cổ cứng", "neck stiffness", "gáy cứng"],
    "shoulder_pain": [
        "đau vai", "vai đau", "shoulder pain"],
    "knee_pain": [
        "đau đầu gối", "gối đau", "knee pain"],
    "hip_pain": [
        "đau hông", "hông đau", "hip pain", "đau háng"],
    "bone_pain": [
        "đau xương", "xương đau", "bone pain"],
    "reduced_range_of_motion": [
        "hạn chế vận động", "cứng cơ", "reduced range of motion"],
    "balance_problems": [
        "mất thăng bằng", "đi không vững", "balance problems"],
    "foot_pain": [
        "đau bàn chân", "bàn chân đau", "foot pain"],
    "gait_disturbance": [
        "rối loạn dáng đi", "đi đứng khó khăn", "gait disturbance"],
    "tophi": [
        "hạt tophi", "cục sưng ở khớp", "tophi", "gút nổi cục"],

    # Skin
    "rash": [
        "phát ban", "ban đỏ", "nổi ban", "rash", "da nổi ban"],
    "skin_redness": [
        "da đỏ", "đỏ da", "skin redness"],
    "itching": [
        "ngứa", "ngứa da", "ngứa ngáy", "itching"],
    "hives": [
        "mề đay", "nổi mề đay", "nổi mẩn ngứa", "hives", "urticaria"],
    "blisters": [
        "phồng rộp", "bọng nước", "blisters", "nước", "mụn nước"],
    "skin_lesions": [
        "tổn thương da", "vết thương da", "skin lesions"],
    "peeling_skin": [
        "bong tróc da", "da bong vảy", "peeling skin"],
    "dry_skin": [
        "da khô", "khô da", "dry skin"],
    "acne": [
        "mụn trứng cá", "mụn", "acne", "nổi mụn"],
    "blackheads": [
        "mụn đầu đen", "blackheads"],
    "pustules": [
        "mụn mủ", "pustules"],
    "skin_thickening": [
        "da dày", "da dày lên", "skin thickening"],
    "skin_discoloration": [
        "thay đổi màu da", "da đổi màu", "skin discoloration"],
    "bruising": [
        "bầm tím", "bầm da", "bruising"],
    "petechiae": [
        "chấm xuất huyết", "ban đỏ nhỏ", "petechiae"],
    "purpura": [
        "ban xuất huyết", "vết xuất huyết dưới da", "purpura"],
    "hair_loss": [
        "rụng tóc", "tóc rụng nhiều", "hair loss", "hói đầu"],
    "nail_changes": [
        "móng thay đổi", "móng dễ gãy", "nail changes"],
    "skin_ulcer": [
        "loét da", "vết loét", "skin ulcer"],
    "wounds_not_healing": [
        "vết thương không lành", "wounds not healing", "lâu lành"],
    "butterfly_rash": [
        "ban dạng bướm", "ban trên má", "butterfly rash"],
    "photosensitivity_skin": [
        "da nhạy cảm ánh sáng", "cháy nắng dễ", "photosensitivity skin"],
    "maculopapular_rash": [
        "ban dát sần", "maculopapular rash", "ban hồng"],
    "vesicular_rash": [
        "ban bọng nước", "mụn nước", "vesicular rash"],
    "spotted_rash": [
        "ban chấm đỏ", "spotted rash", "ban đốm"],
    "acanthosis_nigricans": [
        "da sẫm màu ở nếp gấp", "acanthosis nigricans",
        "nách cổ da sẫm"],

    # Reproductive / Hormonal
    "irregular_menstruation": [
        "kinh nguyệt không đều", "rối loạn kinh nguyệt",
        "irregular menstruation", "chu kỳ kinh không đều"],
    "heavy_menstrual_bleeding": [
        "kinh nguyệt nhiều", "hành kinh nhiều", "heavy menstrual bleeding",
        "cường kinh"],
    "painful_menstruation": [
        "đau bụng kinh", "kinh đau", "painful menstruation", "thống kinh"],
    "absent_menstruation": [
        "mất kinh", "không có kinh", "vô kinh", "absent menstruation",
        "amenorrhea"],
    "vaginal_discharge": [
        "khí hư", "huyết trắng", "vaginal discharge", "dịch âm đạo"],
    "vaginal_bleeding": [
        "xuất huyết âm đạo", "chảy máu âm đạo", "vaginal bleeding"],
    "breast_pain": [
        "đau vú", "vú đau", "breast pain"],
    "breast_lump": [
        "u vú", "cục cứng trong vú", "breast lump"],
    "nipple_discharge": [
        "tiết dịch núm vú", "nipple discharge"],
    "erectile_dysfunction": [
        "rối loạn cương dương", "không cương được", "erectile dysfunction",
        "liệt dương"],
    "testicular_pain": [
        "đau tinh hoàn", "testicular pain"],
    "testicular_swelling": [
        "sưng tinh hoàn", "tinh hoàn sưng", "testicular swelling"],
    "penile_discharge": [
        "tiết dịch dương vật", "penile discharge", "mủ niệu đạo"],
    "increased_thirst": [
        "khát nhiều", "uống nhiều nước", "increased thirst", "polydipsia"],
    "excessive_hunger": [
        "đói nhiều", "ăn nhiều vẫn đói", "excessive hunger", "polyphagia"],
    "heat_intolerance": [
        "không chịu nóng", "nhạy cảm nhiệt", "heat intolerance"],
    "cold_intolerance": [
        "không chịu lạnh", "rét hơn bình thường", "cold intolerance"],
    "goiter": [
        "bướu giáp", "cổ sưng", "goiter", "bướu cổ"],
    "hot_flashes": [
        "bốc hỏa", "hot flashes", "nóng bừng mặt"],
    "cold_sensitivity": [
        "nhạy cảm lạnh", "cold sensitivity", "lạnh hoài"],
    "exophthalmos": [
        "lồi mắt", "mắt lồi", "exophthalmos"],
    "rapid_pulse": [
        "mạch nhanh", "rapid pulse", "mạch đập nhanh"],

    # Mental health
    "low_mood": [
        "tâm trạng thấp", "buồn bã", "low mood", "depressed mood"],
    "hopelessness": [
        "tuyệt vọng", "không có hy vọng", "hopelessness"],
    "panic_attacks": [
        "cơn hoảng loạn", "panic attacks", "lo sợ đột ngột"],
    "excessive_worry": [
        "lo lắng quá mức", "lo âu", "excessive worry", "lo quá"],
    "sleep_disturbance": [
        "rối loạn giấc ngủ", "ngủ không yên", "sleep disturbance"],
    "appetite_changes": [
        "thay đổi khẩu vị", "appetite changes"],
    "loss_of_interest": [
        "mất hứng thú", "không quan tâm", "loss of interest",
        "không thích gì"],
    "social_withdrawal": [
        "thu mình", "tránh xã hội", "social withdrawal", "không muốn gặp ai"],
    "aura": [
        "tiền triệu migraine", "aura", "thấy đèn flash trước đau đầu"],
    "phonophobia": [
        "sợ tiếng ồn", "phonophobia", "âm thanh gây đau"],
    "migraine_headache": [
        "đau nửa đầu", "migraine", "nhức một bên đầu"],
    "nausea_with_headache": [
        "buồn nôn kèm đau đầu", "nausea with headache"],

    # Metabolic / Immune / Other
    "high_cholesterol": [
        "cholesterol cao", "mỡ máu cao", "high cholesterol",
        "rối loạn lipid"],
    "obesity": [
        "béo phì", "thừa cân nhiều", "obesity"],
    "slow_wound_healing": [
        "vết thương lâu lành", "slow wound healing"],
    "easy_bruising": [
        "dễ bầm tím", "hay bầm", "easy bruising"],
    "prolonged_bleeding": [
        "chảy máu kéo dài", "prolonged bleeding"],
    "lump_or_mass": [
        "khối u", "cục u", "lump or mass", "nổi u"],
    "unexplained_weight_loss": [
        "sụt cân không rõ nguyên nhân", "gầy không rõ lý do",
        "unexplained weight loss"],
    "fatigue_cancer": [
        "mệt mỏi kéo dài", "kiệt sức bất thường", "fatigue cancer"],
    "enlarged_liver": [
        "gan to", "gan lớn", "enlarged liver", "hepatomegaly"],
    "enlarged_spleen": [
        "lách to", "enlarged spleen", "splenomegaly"],
    "pleuritis": [
        "viêm màng phổi", "đau khi thở", "pleuritis"],
    "pericarditis": [
        "viêm màng tim", "đau ngực viêm màng", "pericarditis"],
    "proteinuria": [
        "tiểu đạm", "đạm trong nước tiểu", "proteinuria"],
    "fine_tremor": [
        "run nhẹ", "fine tremor", "tay run nhẹ"],
    "bradycardia": [
        "nhịp tim chậm", "bradycardia", "tim đập chậm"],
    "puffy_face": [
        "mặt phù", "mặt sưng phù", "puffy face"],
    "coarse_hair": [
        "tóc thô", "tóc xơ", "coarse hair"],
    "dry_coarse_skin": [
        "da khô thô ráp", "dry coarse skin"],
    "genital_lesions": [
        "tổn thương sinh dục", "loét vùng kín", "genital lesions"],
    "koplik_spots": [
        "nốt koplik", "koplik spots"],
    "spastic_paralysis": [
        "liệt co cứng", "spastic paralysis"],
    "optic_neuritis": [
        "viêm dây thần kinh thị", "optic neuritis", "đau mắt khi cử động"],
    "facial_pain": [
        "đau mặt", "facial pain"],
    "facial_palsy": [
        "liệt mặt", "facial palsy", "méo mặt"],
    "jaw_stiffness": [
        "cứng hàm", "jaw stiffness", "không há miệng được"],
    "risus_sardonicus": [
        "nụ cười cứng", "risus sardonicus"],
    "opisthotonus": [
        "cơ thể uốn cong ra sau", "opisthotonus", "co cứng cung"],
    "kaposi_sarcoma": [
        "ban xuất huyết kaposi", "kaposi sarcoma"],
    "oral_thrush": [
        "nấm miệng", "mảng trắng miệng", "oral thrush"],
    "rose_spots": [
        "ban hồng", "rose spots"],
}

# ──────────────────────────── 100 DISEASES ───────────────────────────────── #
DISEASES: dict[str, dict] = {
    # ── 1-20: Infectious ────────────────────────────────────────────────────
    "influenza": {
        "name_vi": "Cúm (Influenza)",
        "name_en": "Influenza / Flu",
        "symptoms": [
            "fever", "high_fever", "chills", "fatigue", "body_aches",
            "headache", "dry_cough", "sore_throat", "nasal_congestion",
            "runny_nose", "weakness", "sweating",
        ],
    },
    "common_cold": {
        "name_vi": "Cảm lạnh thông thường",
        "name_en": "Common Cold",
        "symptoms": [
            "runny_nose", "nasal_congestion", "sneezing", "sore_throat",
            "dry_cough", "low_grade_fever", "fatigue", "throat_irritation",
            "loss_of_smell",
        ],
    },
    "covid_19": {
        "name_vi": "COVID-19",
        "name_en": "COVID-19",
        "symptoms": [
            "fever", "dry_cough", "fatigue", "loss_of_smell", "shortness_of_breath",
            "body_aches", "headache", "sore_throat", "chills", "diarrhea",
            "nasal_congestion",
        ],
    },
    "pneumonia": {
        "name_vi": "Viêm phổi",
        "name_en": "Pneumonia",
        "symptoms": [
            "fever", "high_fever", "productive_cough", "shortness_of_breath",
            "chest_pain", "chills", "fatigue", "crackles", "rapid_breathing",
            "sweating",
        ],
    },
    "bronchitis": {
        "name_vi": "Viêm phế quản",
        "name_en": "Bronchitis",
        "symptoms": [
            "cough", "productive_cough", "chest_tightness", "fatigue",
            "low_grade_fever", "sore_throat", "nasal_congestion",
            "shortness_of_breath", "wheezing",
        ],
    },
    "tuberculosis": {
        "name_vi": "Lao phổi",
        "name_en": "Tuberculosis",
        "symptoms": [
            "chronic_cough", "coughing_blood", "night_sweats", "weight_loss",
            "fatigue", "low_grade_fever", "loss_of_appetite",
            "hemoptysis", "sputum_production",
        ],
    },
    "dengue_fever": {
        "name_vi": "Sốt xuất huyết Dengue",
        "name_en": "Dengue Fever",
        "symptoms": [
            "high_fever", "severe_headache", "body_aches", "rash",
            "eye_pain", "nausea", "vomiting", "petechiae",
            "easy_bruising", "fatigue",
        ],
    },
    "malaria": {
        "name_vi": "Sốt rét",
        "name_en": "Malaria",
        "symptoms": [
            "fever", "chills", "sweating", "headache", "fatigue",
            "nausea", "vomiting", "body_aches", "jaundice",
            "enlarged_spleen",
        ],
    },
    "typhoid_fever": {
        "name_vi": "Sốt thương hàn",
        "name_en": "Typhoid Fever",
        "symptoms": [
            "fever", "headache", "abdominal_pain", "rose_spots",
            "diarrhea", "constipation", "fatigue", "loss_of_appetite",
            "enlarged_spleen",
        ],
    },
    "cholera": {
        "name_vi": "Tả",
        "name_en": "Cholera",
        "symptoms": [
            "diarrhea", "rice_water_stool", "vomiting", "dehydration",
            "muscle_cramps", "weakness", "rapid_heart_rate",
            "low_blood_pressure",
        ],
    },
    "hepatitis_a": {
        "name_vi": "Viêm gan A",
        "name_en": "Hepatitis A",
        "symptoms": [
            "jaundice", "jaundice_skin", "fatigue", "nausea", "vomiting",
            "abdominal_pain", "loss_of_appetite", "fever", "dark_urine",
            "clay_colored_stool",
        ],
    },
    "hepatitis_b": {
        "name_vi": "Viêm gan B",
        "name_en": "Hepatitis B",
        "symptoms": [
            "jaundice", "fatigue", "abdominal_pain", "loss_of_appetite",
            "nausea", "joint_pain", "dark_urine", "fever",
            "enlarged_liver",
        ],
    },
    "hepatitis_c": {
        "name_vi": "Viêm gan C",
        "name_en": "Hepatitis C",
        "symptoms": [
            "fatigue", "jaundice", "loss_of_appetite", "nausea",
            "abdominal_pain", "dark_urine", "enlarged_liver",
            "joint_pain",
        ],
    },
    "hiv_aids": {
        "name_vi": "HIV/AIDS",
        "name_en": "HIV/AIDS",
        "symptoms": [
            "recurrent_infections", "weight_loss", "fatigue",
            "swollen_lymph_nodes", "oral_thrush", "kaposi_sarcoma",
            "night_sweats", "fever", "diarrhea",
        ],
    },
    "sepsis": {
        "name_vi": "Nhiễm trùng huyết",
        "name_en": "Sepsis",
        "symptoms": [
            "high_fever", "rapid_heart_rate", "rapid_breathing",
            "confusion", "low_blood_pressure", "chills",
            "weakness", "cyanosis",
        ],
    },
    "chickenpox": {
        "name_vi": "Thủy đậu",
        "name_en": "Chickenpox",
        "symptoms": [
            "vesicular_rash", "itching", "fever", "fatigue",
            "loss_of_appetite", "headache", "blisters",
        ],
    },
    "measles": {
        "name_vi": "Sởi",
        "name_en": "Measles",
        "symptoms": [
            "high_fever", "maculopapular_rash", "koplik_spots",
            "cough", "runny_nose", "red_eyes", "light_sensitivity",
            "sore_throat",
        ],
    },
    "mumps": {
        "name_vi": "Quai bị",
        "name_en": "Mumps",
        "symptoms": [
            "parotid_swelling", "fever", "headache", "fatigue",
            "loss_of_appetite", "difficulty_swallowing",
            "testicular_pain",
        ],
    },
    "rubella": {
        "name_vi": "Rubella (Sởi Đức)",
        "name_en": "Rubella",
        "symptoms": [
            "maculopapular_rash", "low_grade_fever", "swollen_lymph_nodes",
            "joint_pain", "headache", "runny_nose", "red_eyes",
        ],
    },
    "tetanus": {
        "name_vi": "Uốn ván",
        "name_en": "Tetanus",
        "symptoms": [
            "jaw_stiffness", "muscle_cramps", "neck_stiffness",
            "risus_sardonicus", "opisthotonus", "fever",
            "difficulty_swallowing", "seizures",
        ],
    },

    # ── 21-30: Cardiovascular ────────────────────────────────────────────────
    "hypertension": {
        "name_vi": "Tăng huyết áp",
        "name_en": "Hypertension",
        "symptoms": [
            "high_blood_pressure", "headache", "dizziness", "blurred_vision",
            "palpitations", "fatigue", "nosebleed", "chest_pain",
        ],
    },
    "heart_attack": {
        "name_vi": "Nhồi máu cơ tim",
        "name_en": "Heart Attack (MI)",
        "symptoms": [
            "chest_pain", "chest_pressure", "arm_pain", "jaw_pain",
            "shortness_of_breath", "sweating", "nausea", "palpitations",
            "fainting",
        ],
    },
    "stroke": {
        "name_vi": "Đột quỵ",
        "name_en": "Stroke",
        "symptoms": [
            "weakness_one_side", "speech_difficulty", "sudden_vision_loss",
            "severe_headache", "dizziness", "confusion",
            "loss_of_consciousness", "facial_palsy",
        ],
    },
    "heart_failure": {
        "name_vi": "Suy tim",
        "name_en": "Heart Failure",
        "symptoms": [
            "shortness_of_breath", "orthopnea", "pedal_edema",
            "fatigue", "leg_swelling", "palpitations",
            "pink_frothy_sputum", "neck_vein_distension",
            "exertional_dyspnea",
        ],
    },
    "atrial_fibrillation": {
        "name_vi": "Rung nhĩ",
        "name_en": "Atrial Fibrillation",
        "symptoms": [
            "irregular_heartbeat", "palpitations", "shortness_of_breath",
            "fatigue", "dizziness", "fainting", "chest_pain",
        ],
    },
    "dvt": {
        "name_vi": "Huyết khối tĩnh mạch sâu",
        "name_en": "Deep Vein Thrombosis",
        "symptoms": [
            "leg_swelling", "calf_pain", "skin_redness",
            "warmth_in_leg", "pedal_edema",
        ],
    },
    "pulmonary_embolism": {
        "name_vi": "Thuyên tắc phổi",
        "name_en": "Pulmonary Embolism",
        "symptoms": [
            "shortness_of_breath", "chest_pain", "rapid_heart_rate",
            "coughing_blood", "fainting", "low_blood_pressure",
            "leg_swelling", "calf_pain",
        ],
    },
    "angina": {
        "name_vi": "Đau thắt ngực",
        "name_en": "Angina Pectoris",
        "symptoms": [
            "chest_pain", "chest_pressure", "exertional_dyspnea",
            "arm_pain", "jaw_pain", "shortness_of_breath",
            "sweating",
        ],
    },
    "peripheral_artery_disease": {
        "name_vi": "Bệnh động mạch ngoại biên",
        "name_en": "Peripheral Artery Disease",
        "symptoms": [
            "calf_pain", "cold_extremities", "foot_pain",
            "skin_discoloration", "wounds_not_healing", "reduced_range_of_motion",
        ],
    },
    "cardiomyopathy": {
        "name_vi": "Bệnh cơ tim",
        "name_en": "Cardiomyopathy",
        "symptoms": [
            "shortness_of_breath", "fatigue", "palpitations",
            "leg_swelling", "dizziness", "fainting",
            "chest_pain",
        ],
    },

    # ── 31-37: Respiratory ──────────────────────────────────────────────────
    "asthma": {
        "name_vi": "Hen suyễn",
        "name_en": "Asthma",
        "symptoms": [
            "wheezing", "shortness_of_breath", "chest_tightness",
            "cough", "dry_cough", "exertional_dyspnea",
            "accessory_muscle_use",
        ],
    },
    "copd": {
        "name_vi": "Bệnh phổi tắc nghẽn mãn tính (COPD)",
        "name_en": "COPD",
        "symptoms": [
            "chronic_cough", "sputum_production", "shortness_of_breath",
            "barrel_chest", "pursed_lip_breathing", "exertional_dyspnea",
            "wheezing", "accessory_muscle_use",
        ],
    },
    "lung_cancer": {
        "name_vi": "Ung thư phổi",
        "name_en": "Lung Cancer",
        "symptoms": [
            "chronic_cough", "hemoptysis", "shortness_of_breath",
            "chest_pain", "weight_loss", "fatigue_cancer",
            "unexplained_weight_loss", "hoarseness",
        ],
    },
    "sleep_apnea": {
        "name_vi": "Ngưng thở khi ngủ",
        "name_en": "Sleep Apnea",
        "symptoms": [
            "excessive_sleepiness", "headache", "insomnia", "fatigue",
            "difficulty_concentrating", "irritability",
            "high_blood_pressure",
        ],
    },
    "pleuritis": {
        "name_vi": "Viêm màng phổi",
        "name_en": "Pleuritis",
        "symptoms": [
            "pleuritic_chest_pain", "shortness_of_breath",
            "fever", "cough", "pleuritis",
        ],
    },
    "pulmonary_fibrosis": {
        "name_vi": "Xơ phổi",
        "name_en": "Pulmonary Fibrosis",
        "symptoms": [
            "shortness_of_breath", "exertional_dyspnea",
            "chronic_cough", "fatigue", "crackles",
            "weight_loss",
        ],
    },
    "bronchiectasis": {
        "name_vi": "Giãn phế quản",
        "name_en": "Bronchiectasis",
        "symptoms": [
            "chronic_cough", "sputum_production", "hemoptysis",
            "shortness_of_breath", "crackles", "recurrent_infections",
        ],
    },

    # ── 38-45: Endocrine / Metabolic ────────────────────────────────────────
    "diabetes_type1": {
        "name_vi": "Đái tháo đường type 1",
        "name_en": "Type 1 Diabetes",
        "symptoms": [
            "increased_thirst", "frequent_urination", "weight_loss",
            "fatigue", "excessive_hunger", "blurred_vision",
            "slow_wound_healing",
        ],
    },
    "diabetes_type2": {
        "name_vi": "Đái tháo đường type 2",
        "name_en": "Type 2 Diabetes",
        "symptoms": [
            "increased_thirst", "frequent_urination", "fatigue",
            "blurred_vision", "slow_wound_healing", "acanthosis_nigricans",
            "obesity", "excessive_hunger", "numbness",
        ],
    },
    "hypothyroidism": {
        "name_vi": "Suy giáp",
        "name_en": "Hypothyroidism",
        "symptoms": [
            "fatigue", "weight_gain", "cold_intolerance", "dry_skin",
            "constipation", "bradycardia", "puffy_face", "coarse_hair",
            "dry_coarse_skin", "cold_sensitivity",
        ],
    },
    "hyperthyroidism": {
        "name_vi": "Cường giáp",
        "name_en": "Hyperthyroidism",
        "symptoms": [
            "weight_loss", "rapid_heart_rate", "heat_intolerance",
            "sweating", "tremors", "fine_tremor", "exophthalmos",
            "goiter", "hot_flashes", "rapid_pulse",
        ],
    },
    "gout": {
        "name_vi": "Bệnh Gút",
        "name_en": "Gout",
        "symptoms": [
            "joint_pain", "joint_swelling", "joint_stiffness",
            "foot_pain", "tophi", "skin_redness", "fever",
        ],
    },
    "hyperlipidemia": {
        "name_vi": "Rối loạn lipid máu",
        "name_en": "Hyperlipidemia",
        "symptoms": [
            "high_cholesterol", "fatigue", "chest_pain",
            "xanthomas", "obesity",
        ],
    },
    "obesity": {
        "name_vi": "Béo phì",
        "name_en": "Obesity",
        "symptoms": [
            "obesity", "weight_gain", "exertional_dyspnea",
            "joint_pain", "high_blood_pressure", "acanthosis_nigricans",
            "sleep_disturbance",
        ],
    },
    "cushings_syndrome": {
        "name_vi": "Hội chứng Cushing",
        "name_en": "Cushing's Syndrome",
        "symptoms": [
            "weight_gain", "obesity", "high_blood_pressure",
            "bruising", "skin_discoloration", "fatigue",
            "irregular_menstruation", "acne",
        ],
    },

    # ── 46-57: Gastrointestinal ──────────────────────────────────────────────
    "gastritis": {
        "name_vi": "Viêm dạ dày",
        "name_en": "Gastritis",
        "symptoms": [
            "upper_abdominal_pain", "nausea", "vomiting", "bloating",
            "indigestion", "loss_of_appetite", "heartburn",
        ],
    },
    "peptic_ulcer": {
        "name_vi": "Loét dạ dày - tá tràng",
        "name_en": "Peptic Ulcer Disease",
        "symptoms": [
            "upper_abdominal_pain", "pain_relieved_by_eating",
            "pain_after_eating", "nausea", "dark_stool",
            "vomiting", "heartburn", "loss_of_appetite",
        ],
    },
    "appendicitis": {
        "name_vi": "Viêm ruột thừa",
        "name_en": "Appendicitis",
        "symptoms": [
            "right_lower_abdominal_pain", "fever", "nausea",
            "vomiting", "loss_of_appetite", "abdominal_pain",
        ],
    },
    "irritable_bowel_syndrome": {
        "name_vi": "Hội chứng ruột kích thích (IBS)",
        "name_en": "Irritable Bowel Syndrome",
        "symptoms": [
            "abdominal_pain", "bloating", "diarrhea", "constipation",
            "mucus_in_stool", "stomach_cramps", "gas",
        ],
    },
    "gerd": {
        "name_vi": "Trào ngược dạ dày - thực quản (GERD)",
        "name_en": "GERD",
        "symptoms": [
            "heartburn", "acid_reflux", "chest_pain", "hoarseness",
            "difficulty_swallowing", "nausea", "bloating",
        ],
    },
    "pancreatitis": {
        "name_vi": "Viêm tụy",
        "name_en": "Pancreatitis",
        "symptoms": [
            "upper_abdominal_pain", "nausea", "vomiting", "fever",
            "abdominal_distension", "loss_of_appetite", "jaundice",
        ],
    },
    "gallstones": {
        "name_vi": "Sỏi mật",
        "name_en": "Gallstones",
        "symptoms": [
            "upper_abdominal_pain", "jaundice", "nausea", "vomiting",
            "fever", "clay_colored_stool", "dark_urine",
        ],
    },
    "cirrhosis": {
        "name_vi": "Xơ gan",
        "name_en": "Liver Cirrhosis",
        "symptoms": [
            "jaundice", "ascites", "enlarged_spleen", "easy_bruising",
            "fatigue", "loss_of_appetite", "spider_angioma_skin",
            "cognitive_decline",
        ],
    },
    "colon_cancer": {
        "name_vi": "Ung thư đại tràng",
        "name_en": "Colon Cancer",
        "symptoms": [
            "bloody_stool", "rectal_bleeding", "abdominal_pain",
            "weight_loss", "fatigue_cancer", "constipation",
            "diarrhea", "lump_or_mass",
        ],
    },
    "stomach_cancer": {
        "name_vi": "Ung thư dạ dày",
        "name_en": "Stomach Cancer",
        "symptoms": [
            "upper_abdominal_pain", "loss_of_appetite", "weight_loss",
            "nausea", "vomiting", "dark_stool", "fatigue_cancer",
            "bloating",
        ],
    },
    "liver_cancer": {
        "name_vi": "Ung thư gan",
        "name_en": "Liver Cancer",
        "symptoms": [
            "upper_abdominal_pain", "jaundice", "weight_loss",
            "fatigue_cancer", "enlarged_liver", "ascites",
            "loss_of_appetite",
        ],
    },
    "celiac_disease": {
        "name_vi": "Bệnh celiac",
        "name_en": "Celiac Disease",
        "symptoms": [
            "diarrhea", "bloating", "abdominal_pain", "weight_loss",
            "fatigue", "skin_redness", "constipation",
        ],
    },

    # ── 58-67: Neurological ─────────────────────────────────────────────────
    "migraine": {
        "name_vi": "Đau nửa đầu (Migraine)",
        "name_en": "Migraine",
        "symptoms": [
            "migraine_headache", "nausea_with_headache", "vomiting",
            "light_sensitivity", "phonophobia", "aura",
            "blurred_vision",
        ],
    },
    "epilepsy": {
        "name_vi": "Động kinh",
        "name_en": "Epilepsy",
        "symptoms": [
            "seizures", "loss_of_consciousness", "confusion",
            "fatigue", "mood_changes", "memory_loss",
        ],
    },
    "alzheimers": {
        "name_vi": "Bệnh Alzheimer",
        "name_en": "Alzheimer's Disease",
        "symptoms": [
            "memory_loss", "cognitive_decline", "personality_changes",
            "agitation", "word_finding_difficulty", "confusion",
            "social_withdrawal", "loss_of_interest",
        ],
    },
    "parkinsons": {
        "name_vi": "Bệnh Parkinson",
        "name_en": "Parkinson's Disease",
        "symptoms": [
            "tremors", "pill_rolling_tremor", "slow_movements",
            "shuffling_gait", "mask_face", "stooped_posture",
            "balance_problems", "gait_disturbance",
        ],
    },
    "multiple_sclerosis": {
        "name_vi": "Xơ cứng rải rác (MS)",
        "name_en": "Multiple Sclerosis",
        "symptoms": [
            "fatigue", "numbness", "tingling", "weakness",
            "blurred_vision", "optic_neuritis", "balance_problems",
            "spastic_paralysis", "double_vision",
        ],
    },
    "meningitis": {
        "name_vi": "Viêm màng não",
        "name_en": "Meningitis",
        "symptoms": [
            "severe_headache", "neck_stiffness", "high_fever",
            "light_sensitivity", "nausea", "vomiting",
            "confusion", "rash", "petechiae",
        ],
    },
    "encephalitis": {
        "name_vi": "Viêm não",
        "name_en": "Encephalitis",
        "symptoms": [
            "fever", "severe_headache", "confusion", "seizures",
            "loss_of_consciousness", "weakness", "vision_changes",
        ],
    },
    "peripheral_neuropathy": {
        "name_vi": "Bệnh thần kinh ngoại biên",
        "name_en": "Peripheral Neuropathy",
        "symptoms": [
            "numbness", "tingling", "weakness", "foot_pain",
            "balance_problems", "muscle_weakness",
        ],
    },
    "transient_ischemic_attack": {
        "name_vi": "Cơn thiếu máu não thoáng qua (TIA)",
        "name_en": "Transient Ischemic Attack",
        "symptoms": [
            "weakness_one_side", "speech_difficulty", "dizziness",
            "sudden_vision_loss", "confusion", "numbness",
        ],
    },
    "guillain_barre": {
        "name_vi": "Hội chứng Guillain-Barré",
        "name_en": "Guillain-Barré Syndrome",
        "symptoms": [
            "weakness", "paralysis", "tingling", "numbness",
            "muscle_weakness", "gait_disturbance", "facial_palsy",
        ],
    },

    # ── 68-72: Mental Health ─────────────────────────────────────────────────
    "major_depression": {
        "name_vi": "Trầm cảm nặng",
        "name_en": "Major Depressive Disorder",
        "symptoms": [
            "low_mood", "hopelessness", "loss_of_interest",
            "insomnia", "fatigue", "social_withdrawal",
            "appetite_changes", "difficulty_concentrating",
        ],
    },
    "anxiety_disorder": {
        "name_vi": "Rối loạn lo âu",
        "name_en": "Generalized Anxiety Disorder",
        "symptoms": [
            "excessive_worry", "insomnia", "fatigue", "muscle_pain",
            "irritability", "difficulty_concentrating", "panic_attacks",
            "palpitations",
        ],
    },
    "insomnia_disorder": {
        "name_vi": "Mất ngủ mãn tính",
        "name_en": "Chronic Insomnia",
        "symptoms": [
            "insomnia", "fatigue", "difficulty_concentrating",
            "mood_changes", "irritability", "excessive_worry",
            "sleep_disturbance",
        ],
    },
    "bipolar_disorder": {
        "name_vi": "Rối loạn lưỡng cực",
        "name_en": "Bipolar Disorder",
        "symptoms": [
            "mood_changes", "insomnia", "increased_appetite",
            "agitation", "irritability", "low_mood",
            "excessive_sleepiness",
        ],
    },
    "schizophrenia": {
        "name_vi": "Tâm thần phân liệt",
        "name_en": "Schizophrenia",
        "symptoms": [
            "hallucinations", "social_withdrawal", "loss_of_interest",
            "agitation", "confusion", "sleep_disturbance",
            "cognitive_decline",
        ],
    },

    # ── 73-81: Musculoskeletal ───────────────────────────────────────────────
    "osteoarthritis": {
        "name_vi": "Viêm xương khớp (thoái hóa)",
        "name_en": "Osteoarthritis",
        "symptoms": [
            "joint_pain", "joint_stiffness", "knee_pain", "hip_pain",
            "reduced_range_of_motion", "bone_pain",
            "gait_disturbance",
        ],
    },
    "rheumatoid_arthritis": {
        "name_vi": "Viêm khớp dạng thấp",
        "name_en": "Rheumatoid Arthritis",
        "symptoms": [
            "joint_pain", "joint_swelling", "morning_stiffness",
            "fatigue", "fever", "weight_loss",
            "joint_stiffness", "shoulder_pain",
        ],
    },
    "osteoporosis": {
        "name_vi": "Loãng xương",
        "name_en": "Osteoporosis",
        "symptoms": [
            "back_pain", "bone_pain", "reduced_range_of_motion",
            "stooped_posture", "height_loss",
        ],
    },
    "low_back_pain": {
        "name_vi": "Đau lưng dưới",
        "name_en": "Low Back Pain",
        "symptoms": [
            "lower_back_pain", "muscle_pain", "reduced_range_of_motion",
            "numbness", "tingling", "back_pain",
        ],
    },
    "cervical_spondylosis": {
        "name_vi": "Thoái hóa cột sống cổ",
        "name_en": "Cervical Spondylosis",
        "symptoms": [
            "neck_pain", "neck_stiffness", "shoulder_pain", "headache",
            "numbness", "tingling", "weakness",
        ],
    },
    "herniated_disc": {
        "name_vi": "Thoát vị đĩa đệm",
        "name_en": "Herniated Disc",
        "symptoms": [
            "lower_back_pain", "numbness", "tingling", "leg_pain",
            "muscle_weakness", "reduced_range_of_motion",
        ],
    },
    "fibromyalgia": {
        "name_vi": "Hội chứng đau xơ cơ",
        "name_en": "Fibromyalgia",
        "symptoms": [
            "muscle_pain", "fatigue", "insomnia", "headache",
            "joint_pain", "difficulty_concentrating", "mood_changes",
        ],
    },
    "ankylosing_spondylitis": {
        "name_vi": "Viêm cột sống dính khớp",
        "name_en": "Ankylosing Spondylitis",
        "symptoms": [
            "lower_back_pain", "morning_stiffness", "back_pain",
            "hip_pain", "fatigue", "reduced_range_of_motion",
        ],
    },
    "bursitis": {
        "name_vi": "Viêm túi hoạt dịch",
        "name_en": "Bursitis",
        "symptoms": [
            "joint_pain", "joint_swelling", "joint_stiffness",
            "shoulder_pain", "hip_pain", "knee_pain",
        ],
    },

    # ── 82-86: Kidney / Urinary ──────────────────────────────────────────────
    "kidney_stones": {
        "name_vi": "Sỏi thận",
        "name_en": "Kidney Stones",
        "symptoms": [
            "flank_pain", "kidney_pain", "painful_urination",
            "blood_in_urine", "nausea", "vomiting",
            "frequent_urination",
        ],
    },
    "urinary_tract_infection": {
        "name_vi": "Nhiễm trùng đường tiểu",
        "name_en": "Urinary Tract Infection",
        "symptoms": [
            "painful_urination", "burning_urination", "frequent_urination",
            "cloudy_urine", "fever", "pelvic_pain", "dark_urine",
        ],
    },
    "chronic_kidney_disease": {
        "name_vi": "Bệnh thận mãn tính",
        "name_en": "Chronic Kidney Disease",
        "symptoms": [
            "decreased_urine_output", "fatigue", "leg_swelling",
            "high_blood_pressure", "nausea", "loss_of_appetite",
            "proteinuria",
        ],
    },
    "nephrotic_syndrome": {
        "name_vi": "Hội chứng thận hư",
        "name_en": "Nephrotic Syndrome",
        "symptoms": [
            "leg_swelling", "pedal_edema", "proteinuria",
            "fatigue", "loss_of_appetite", "abdominal_distension",
        ],
    },
    "benign_prostatic_hyperplasia": {
        "name_vi": "Phì đại lành tính tuyến tiền liệt",
        "name_en": "Benign Prostatic Hyperplasia",
        "symptoms": [
            "difficulty_urinating", "nocturia", "frequent_urination",
            "urinary_incontinence", "decreased_urine_output",
        ],
    },

    # ── 87-94: Skin ──────────────────────────────────────────────────────────
    "acne_vulgaris": {
        "name_vi": "Mụn trứng cá",
        "name_en": "Acne Vulgaris",
        "symptoms": [
            "acne", "blackheads", "pustules", "skin_redness",
            "oily_skin", "skin_lesions",
        ],
    },
    "psoriasis": {
        "name_vi": "Bệnh vảy nến",
        "name_en": "Psoriasis",
        "symptoms": [
            "peeling_skin", "skin_redness", "itching",
            "skin_thickening", "nail_changes", "joint_pain",
        ],
    },
    "eczema_atopic": {
        "name_vi": "Chàm (viêm da cơ địa)",
        "name_en": "Atopic Dermatitis (Eczema)",
        "symptoms": [
            "itching", "rash", "dry_skin", "skin_redness",
            "blisters", "peeling_skin",
        ],
    },
    "urticaria_allergic": {
        "name_vi": "Mề đay dị ứng",
        "name_en": "Allergic Urticaria",
        "symptoms": [
            "hives", "itching", "rash", "skin_redness",
            "swollen_eyelids", "throat_swelling",
        ],
    },
    "ringworm": {
        "name_vi": "Nấm da (hắc lào)",
        "name_en": "Ringworm (Tinea)",
        "symptoms": [
            "rash", "itching", "skin_redness", "peeling_skin",
            "skin_lesions",
        ],
    },
    "scabies_infection": {
        "name_vi": "Ghẻ",
        "name_en": "Scabies",
        "symptoms": [
            "itching", "rash", "blisters", "skin_redness",
            "skin_lesions",
        ],
    },
    "cellulitis": {
        "name_vi": "Viêm mô tế bào",
        "name_en": "Cellulitis",
        "symptoms": [
            "skin_redness", "skin_swelling", "fever", "warmth_in_skin",
            "skin_pain", "fatigue",
        ],
    },
    "melanoma": {
        "name_vi": "Ung thư hắc tố",
        "name_en": "Melanoma",
        "symptoms": [
            "skin_lesions", "skin_discoloration", "lump_or_mass",
            "skin_ulcer", "itching",
        ],
    },

    # ── 95-100: Eyes / ENT ───────────────────────────────────────────────────
    "glaucoma": {
        "name_vi": "Tăng nhãn áp (Glaucoma)",
        "name_en": "Glaucoma",
        "symptoms": [
            "eye_pressure", "tunnel_vision", "gradual_vision_loss",
            "headache", "eye_pain", "halos_around_lights",
        ],
    },
    "cataracts": {
        "name_vi": "Đục thủy tinh thể",
        "name_en": "Cataracts",
        "symptoms": [
            "blurred_vision", "gradual_vision_loss", "double_vision",
            "light_sensitivity", "halos_around_lights",
            "vision_changes",
        ],
    },
    "conjunctivitis": {
        "name_vi": "Viêm kết mạc (đau mắt đỏ)",
        "name_en": "Conjunctivitis",
        "symptoms": [
            "red_eyes", "eye_discharge", "eye_itching",
            "swollen_eyelids", "light_sensitivity",
        ],
    },
    "otitis_media": {
        "name_vi": "Viêm tai giữa",
        "name_en": "Otitis Media",
        "symptoms": [
            "ear_pain", "fever", "hearing_loss", "ear_discharge",
            "headache", "irritability",
        ],
    },
    "sinusitis": {
        "name_vi": "Viêm xoang",
        "name_en": "Sinusitis",
        "symptoms": [
            "nasal_congestion", "facial_pain", "headache",
            "runny_nose", "loss_of_smell", "fever",
            "throat_irritation",
        ],
    },
    "tonsillitis": {
        "name_vi": "Viêm amidan",
        "name_en": "Tonsillitis",
        "symptoms": [
            "sore_throat", "fever", "difficulty_swallowing",
            "throat_swelling", "headache", "fatigue",
            "swollen_lymph_nodes",
        ],
    },
}
