document.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (window.scrollY > 30) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }
});

// Handle New Assessment button - scroll after reset
document.addEventListener('DOMContentLoaded', function() {
    function setupNewAssessmentButton() {
        const newAssessmentBtn = document.getElementById('new-assessment-button');
        if (newAssessmentBtn && !newAssessmentBtn.hasAttribute('data-scroll-setup')) {
            newAssessmentBtn.setAttribute('data-scroll-setup', 'true');
            newAssessmentBtn.addEventListener('click', function(e) {
                // Wait for the reset callback to complete, then scroll
                setTimeout(function() {
                    const patientSection = document.getElementById('patient-details-section');
                    if (patientSection) {
                        patientSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                }, 500);
            });
        }
    }
    
    setTimeout(setupNewAssessmentButton, 100);
    
    // Watch for new assessment button
    const newAssessmentObserver = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length > 0) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) {
                        if (node.id === 'new-assessment-button' || node.querySelector('#new-assessment-button')) {
                            setTimeout(setupNewAssessmentButton, 100);
                        }
                    }
                });
            }
        });
    });
    
    newAssessmentObserver.observe(document.body, {
        childList: true,
        subtree: true
    });
});

// Export report functionality
document.addEventListener('DOMContentLoaded', function() {
    function setupExportButton() {
        const exportBtn = document.getElementById('export-report-button');
        if (exportBtn && !exportBtn.hasAttribute('data-export-setup')) {
            exportBtn.setAttribute('data-export-setup', 'true');
            exportBtn.addEventListener('click', function() {
                const reportDataEl = document.getElementById('report-data-store');
                if (reportDataEl) {
                    const reportData = reportDataEl.textContent || reportDataEl.getAttribute('data-report');
                    if (reportData) {
                        try {
                            const data = JSON.parse(reportData);
                            let reportText = "=".repeat(60) + "\n";
                            reportText += "HEART DISEASE RISK ASSESSMENT REPORT\n";
                            reportText += "=".repeat(60) + "\n\n";
                            reportText += `Assessment Date: ${data.risk_assessment['Assessment Date']}\n\n`;
                            reportText += "PATIENT DETAILS\n";
                            reportText += "-".repeat(60) + "\n";
                            for (const [key, value] of Object.entries(data.patient_details)) {
                                reportText += `${key}: ${value}\n`;
                            }
                            reportText += "\n";
                            reportText += "RISK ASSESSMENT\n";
                            reportText += "-".repeat(60) + "\n";
                            reportText += `Risk Probability: ${data.risk_assessment['Risk Probability']}\n`;
                            reportText += `Risk Level: ${data.risk_assessment['Risk Level']}\n`;
                            reportText += "\n" + "=".repeat(60) + "\n";
                            
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
                    }
                }
            });
        }
    }
    
    // Setup on load
    setTimeout(setupExportButton, 100);
    
    // Watch for new export buttons
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length > 0) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) {
                        if (node.id === 'export-report-button' || node.querySelector('#export-report-button')) {
                            setTimeout(setupExportButton, 100);
                        }
                    }
                });
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});

// Make entire radio button bar clickable and ensure only one selection per group
document.addEventListener('DOMContentLoaded', function() {
    // Function to handle radio button clicks - make entire bar clickable
    function makeRadioButtonsClickable() {
        // Get all radio button groups (each RadioItems component creates a group)
        const radioGroups = document.querySelectorAll('.radio-buttons');
        
        radioGroups.forEach(function(radioGroup) {
            const radioButtons = radioGroup.querySelectorAll('.form-check');
            
            radioButtons.forEach(function(radioButton) {
                const radioInput = radioButton.querySelector('input[type="radio"]');
                
                if (radioInput && !radioButton.hasAttribute('data-clickable')) {
                    // Mark as processed
                    radioButton.setAttribute('data-clickable', 'true');
                    
                    // Make the entire form-check div clickable
                    radioButton.style.cursor = 'pointer';
                    
                    // Make the entire bar clickable
                    radioButton.addEventListener('click', function(e) {
                        // If clicking on the bar (not directly on input), select the radio
                        if (e.target !== radioInput && e.target.tagName !== 'INPUT' && e.target.tagName !== 'LABEL') {
                            e.preventDefault();
                            e.stopPropagation();
                            
                            // Get the name attribute to find all radio buttons in the same group
                            const radioName = radioInput.name;
                            
                            // Uncheck all radio buttons in the same group first
                            const allRadiosInGroup = document.querySelectorAll(`input[type="radio"][name="${radioName}"]`);
                            allRadiosInGroup.forEach(function(radio) {
                                if (radio !== radioInput) {
                                    radio.checked = false;
                                }
                            });
                            
                            // Check the clicked radio button
                            radioInput.checked = true;
                            
                            // Trigger change event for Dash
                            radioInput.dispatchEvent(new Event('change', { bubbles: true }));
                            radioInput.dispatchEvent(new Event('input', { bubbles: true }));
                        }
                    });
                    
                    // Ensure native radio button behavior works (uncheck others in group)
                    radioInput.addEventListener('change', function(e) {
                        const radioName = radioInput.name;
                        const allRadiosInGroup = document.querySelectorAll(`input[type="radio"][name="${radioName}"]`);
                        allRadiosInGroup.forEach(function(radio) {
                            if (radio !== radioInput && radio.checked) {
                                radio.checked = false;
                            }
                        });
                    });
                }
            });
        });
    }
    
    // Run on page load
    setTimeout(makeRadioButtonsClickable, 200);
    
    // Also run when Dash updates the DOM
    const observer = new MutationObserver(function(mutations) {
        let shouldRerun = false;
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length > 0) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) {
                        if (node.classList && (node.classList.contains('form-check') || node.classList.contains('radio-buttons'))) {
                            shouldRerun = true;
                        } else if (node.querySelector && node.querySelector('.form-check, .radio-buttons')) {
                            shouldRerun = true;
                        }
                    }
                });
            }
        });
        if (shouldRerun) {
            setTimeout(makeRadioButtonsClickable, 200);
        }
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});