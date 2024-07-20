
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.List;
import java.util.regex.*;
import java.util.concurrent.*;


class Extractor {
    private String inputfile;
    private String outputfile;
    private List<String> sections;
    private List<String> sectionNames;
    private Map<String, String> substrings;


    public List<String> getSections() {
		return sections;
	}

	public void setSections(List<String> sections) {
		this.sections = sections;
	}

	public List<String> getSectionNames() {
		return sectionNames;
	}

	public void setSectionNames(List<String> sectionNames) {
		this.sectionNames = sectionNames;
	}

	public Map<String, String> getSubstrings() {
		return substrings;
	}

	public void setSubstrings(Map<String, String> substrings) {
		this.substrings = substrings;
	}


    public Extractor(String inputfile, String outputfile, Map<String, String> substrings) {
        this.inputfile = inputfile;
        this.outputfile = outputfile;
        this.substrings = substrings;
        this.sections = new ArrayList<>();
        this.sectionNames = new ArrayList<>();
    }

    public void extractSections(String expression) throws IOException {
        Pattern pattern = Pattern.compile(expression);
        List<String> currentSectionLines = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(this.inputfile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                Matcher matcher = pattern.matcher(line);
                if (matcher.find()) {
                    if (!currentSectionLines.isEmpty()) {
                        this.sections.add(String.join("\n", currentSectionLines));
                        currentSectionLines.clear();
                    }
                    try {
                        currentSectionLines.add(line);
                        System.out.println(matcher.group(0));
                        this.sectionNames.add(matcher.group(0).trim());

                    }catch(Exception ex) {
                        ex.printStackTrace();
                    }
                   
                } else {
                    currentSectionLines.add(line);
                }
            }
            if (!currentSectionLines.isEmpty()) {
                this.sections.add(String.join("\n", currentSectionLines));
            }
        }
    }

    public boolean checkPassed() throws IOException {
        try (BufferedReader reader = new BufferedReader(new FileReader(this.inputfile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.contains("*  P A S S  *")) {
                    return true;
                }
            }
        }
        return false;
    }

    public String checkFailed() {
        String error = "";
        for (int i = 0; i < this.sections.size(); i++) {
            String section = this.sections.get(i);
            String name = this.sectionNames.get(i);
            String[] lines = section.split("\n");
            for (String line : lines) {
                if (line.contains("--- [Failed]  :")) {
                    error = line.split(":")[1].trim() + " : " + name;
                    break;
                }
                if (line.contains(")  --- [Failed]")) {
                    error = line.split(":")[0].trim() + " : " + name;
                    break;
                }
            }
            if (!error.isEmpty()) {
                break;
            }
        }
        return error;
    }

    public void extractMeasurements(List<String> results, String sectionContent, String sectionName, String expression) {
        Pattern pattern = Pattern.compile(expression);
        String[] lines = sectionContent.split("\n");
        for (String line : lines) {
            Matcher matcher = pattern.matcher(line);
            sectionName = sectionName.replace('.', '_');
            if (matcher.find()) {
                String measurementName = sectionName;
                String description = matcher.group(1).trim();
                String value = matcher.group(2).trim();
                String unit = matcher.group(3).trim();
                String limits = matcher.group(4).trim();
                double lowerLimit = Double.NaN;
                double higherLimit = Double.NaN;

                Matcher limitMatcher = Pattern.compile("\\s*(-?\\d+(\\.\\d+)?)?\\s*,?\\s*(-?\\d+(\\.\\d+)?)?\\s*").matcher(limits);
                if (limitMatcher.find()) {
                    String lowerLimitStr = limitMatcher.group(1);
                    String higherLimitStr = limitMatcher.group(3);
                    if (lowerLimitStr != null) {
                        lowerLimit = Double.parseDouble(lowerLimitStr);
                    } else {
                        lowerLimit = unit.equals("%") ? 0 : -999;
                    }
                    if (higherLimitStr != null) {
                        higherLimit = Double.parseDouble(higherLimitStr);
                    } else {
                        higherLimit = unit.equals("%") ? 100 : 999;
                    }
                    if (higherLimit == 0) {
                        higherLimit = 100;
                    }
                }
                //System.out.println(  measurementName.split("_______")[0]  );
                String name  = String.format("%s", measurementName.split("_______")[0]);


                try {

                    if(name.indexOf("_RXTX_", 0)!=-1)
                    name.replace("_RXTX_", "");
                    else  if (name.indexOf("_TXTX__", 0)!=-1)
                    name.replace("_TXTX__", "");

                    System.out.println(name);


                }catch(Exception ex) {ex.printStackTrace();}



                results.add(String.format("Nom: %s Measurement: %s Unit: %s LowerLimit: %s, HigherLimit: %s, Description: %s",
                        name, value, unit, lowerLimit, higherLimit, description));
            }
        }
    }

    public String removeSubstrings(String inputString) {
        for (Map.Entry<String, String> entry : this.substrings.entrySet()) {
            inputString = inputString.replace(entry.getKey(), entry.getValue());
        }
        return inputString;
    }

    public static Map<String, String> retsubstring() {
        Map<String, String> substrings = new HashMap<>();
        substrings.put("_VERIFY", "TX");
        substrings.put("EVM", "");
        substrings.put("MASK", "");
        substrings.put("SPECTRUM", "");
        substrings.put("EHT_MU", "");
        substrings.put("TEST", "");
        substrings.put(" ", "_");
        substrings.put("-", "");
        substrings.put("IMPLICIT", "IMP");
        substrings.put("BEAMFORMING", "BMF");
        substrings.put("CALIBRATION", "CAL");
        substrings.put("__POWER_", "");
        substrings.put("__", "_");
        substrings.put("PER_", "RX");
        substrings.put("_HE_SU", "");
        substrings.put("__5", "_5");
        substrings.put("TXTX", "TX_");
        substrings.put("RXTX", "");
        substrings.put("_RX", "RX_");
        substrings.put("_RXTX", "");
        return substrings;
    }
}

public class ExtractorUi extends JFrame {
    private JTextField inputFileField;
    private JTextField outputFileField;
    private JTextArea resultsArea;
    private JFileChooser fileChooser;
    private Extractor extractor;

 

    public ExtractorUi() {
        setTitle("Extractor UI");
        setSize(600, 400);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        JPanel panel = new JPanel(new GridLayout(3, 3));

        // Input file
        JLabel inputFileLabel = new JLabel("Input File:");
        inputFileField = new JTextField();
        JButton inputFileButton = new JButton("Browse");
        inputFileButton.addActionListener(e -> chooseFile(inputFileField));

        // Output file
        JLabel outputFileLabel = new JLabel("Output File:");
        outputFileField = new JTextField();
        JButton outputFileButton = new JButton("Browse");
        outputFileButton.addActionListener(e -> chooseFile(outputFileField));

        // Add components to the panel
        panel.add(inputFileLabel);
        panel.add(inputFileField);
        panel.add(inputFileButton);
        panel.add(outputFileLabel);
        panel.add(outputFileField);
        panel.add(outputFileButton);

        // Results area
        resultsArea = new JTextArea();
        resultsArea.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(resultsArea);

        // Extract button
        JButton extractButton = new JButton("Extract");
        extractButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    extractData();
                } catch (IOException | InterruptedException | ExecutionException ex) {
                    ex.printStackTrace();
                }
            }
        });

        // Add components to the frame
        add(panel, BorderLayout.NORTH);
        add(scrollPane, BorderLayout.CENTER);
        add(extractButton, BorderLayout.SOUTH);

        fileChooser = new JFileChooser();
    }

    private void chooseFile(JTextField textField) {
        int returnValue = fileChooser.showOpenDialog(this);
        if (returnValue == JFileChooser.APPROVE_OPTION) {
            File selectedFile = fileChooser.getSelectedFile();
            textField.setText(selectedFile.getAbsolutePath());
        }
    }

    private void extractData() throws IOException, InterruptedException, ExecutionException {
        String inputFile = inputFileField.getText();
        String outputFile = outputFileField.getText();
        Map<String, String> substrings = Extractor.retsubstring();

        extractor = new Extractor(inputFile, outputFile, substrings);

        if (!Files.exists(Paths.get(inputFile))) {
            resultsArea.setText("Input file does not exist.");
            return;
        }

        extractor.extractSections("^\\d+\\..*?_{3,}");

        boolean passed = extractor.checkPassed();
        List<String> results = new ArrayList<>();

        if (!passed) {
            String error = extractor.checkFailed();
            results.add("FAILED: " + error);
        }

        for (int i = 0; i < extractor.getSectionNames().size(); i++) {
            String sectionName = extractor.removeSubstrings(extractor.getSectionNames().get(i));
            extractor.extractMeasurements(results, extractor.getSections().get(i), sectionName, "^([\\w\\s]+)\\s+:\\s+([-+]?\\d*\\.?\\d+)\\s+([\\w%]+)\\s+\\((.*?)\\)");
        }

        ExecutorService executor = Executors.newSingleThreadExecutor();
        Future<?> future = executor.submit(() -> {
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile))) {
                for (String result : results) {
                    writer.write(result);
                    writer.newLine();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        });

        future.get();
        executor.shutdown();

        // Display the results in the text area
        resultsArea.setText(String.join("\n", results));
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            ExtractorUi extractorUI = new ExtractorUi();
            extractorUI.setVisible(true);
        });
    }
}
