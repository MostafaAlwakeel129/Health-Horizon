// Export report functionality
window.exportReport = function(reportData) {
    try {
        const data = JSON.parse(reportData);
        
        // Create report text
        let reportText = "=".repeat(60) + "\n";
        reportText += "HEART DISEASE RISK ASSESSMENT REPORT\n";
        reportText += "=".repeat(60) + "\n\n";
        reportText += `Assessment Date: ${data.risk_assessment.Assessment_Date}\n\n`;
        reportText += "PATIENT DETAILS\n";
        reportText += "-".repeat(60) + "\n";
        
        for (const [key, value] of Object.entries(data.patient_details)) {
            reportText += `${key}: ${value}\n`;
        }
        
        reportText += "\n";
        reportText += "RISK ASSESSMENT\n";
        reportText += "-".repeat(60) + "\n";
        reportText += `Risk Probability: ${data.risk_assessment.Risk_Probability}\n`;
        reportText += `Risk Level: ${data.risk_assessment.Risk_Level}\n`;
        reportText += "\n" + "=".repeat(60) + "\n";
        
        // Create blob and download
        const blob = new Blob([reportText], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Heart_Disease_Assessment_${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Error exporting report:', error);
        alert('Error exporting report. Please try again.');
    }
};

