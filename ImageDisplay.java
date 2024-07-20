import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;

public class ImageDisplay extends JFrame {
    private BufferedImage image;

    public ImageDisplay() {
        try {
            // Load the image
            image = ImageIO.read(new File("./image1.jpeg"));

        } catch (IOException e) {
            e.printStackTrace();
        }

        // Set the title of the window
        setTitle("Image Display");

        // Set the size of the window
        setSize(new Dimension(image.getWidth(), image.getHeight()));

        // Ensure the program exits when the window is closed
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Make the window visible
        setVisible(true);
    }

    @Override
    public void paint(Graphics g) {
        super.paint(g);
        // Draw the image
        g.drawImage(image, 0, 0, null);
    }

    public static void main(String[] args) {
        // Create an instance of the ImageDisplay class
        SwingUtilities.invokeLater(() -> new ImageDisplay());
    }
}
